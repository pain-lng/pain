// Pain Language VS Code Extension

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { exec } from 'child_process';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
    TransportKind
} from 'vscode-languageclient/node';

// Suppress punycode deprecation warning if possible
if (process.emitWarning) {
    const originalEmitWarning = process.emitWarning;
    process.emitWarning = function(warning: any, ...args: any[]) {
        if (typeof warning === 'string' && warning.includes('punycode')) {
            return false; // Suppress punycode warnings
        }
        return originalEmitWarning.call(process, warning, ...args);
    };
}

let client: LanguageClient;

export function activate(context: vscode.ExtensionContext) {
    try {
        // Get workspace folders (may be undefined if no workspace is open)
        const workspaceFolders = vscode.workspace.workspaceFolders;
        
        // Get LSP server path from configuration or use default
        // getConfiguration can be called without workspace, it returns default values
        let lspPath = '';
        try {
            const config = vscode.workspace.getConfiguration('pain');
            lspPath = config.get<string>('lsp.path', '') || '';
        } catch (error) {
            // If configuration fails, use default empty string
            console.warn('Failed to get configuration, using defaults:', error);
        }
        
        // If not configured, try to find pain-lsp in workspace or PATH
        if (!lspPath) {
            // Try relative path from workspace root (only if workspace is open)
            if (workspaceFolders && workspaceFolders.length > 0) {
                const workspaceRoot = workspaceFolders[0].uri.fsPath;
                // Try target/debug/pain-lsp (development)
                const devPath = path.join(workspaceRoot, 'target', 'debug', 'pain-lsp');
                const devPathExe = devPath + (process.platform === 'win32' ? '.exe' : '');
                if (fs.existsSync(devPathExe)) {
                    lspPath = devPathExe;
                } else if (fs.existsSync(devPath)) {
                    lspPath = devPath;
                } else {
                    // Try target/release/pain-lsp (release)
                    const releasePath = path.join(workspaceRoot, 'target', 'release', 'pain-lsp');
                    const releasePathExe = releasePath + (process.platform === 'win32' ? '.exe' : '');
                    if (fs.existsSync(releasePathExe)) {
                        lspPath = releasePathExe;
                    } else if (fs.existsSync(releasePath)) {
                        lspPath = releasePath;
                    } else {
                        // Fallback to 'pain-lsp' in PATH
                        lspPath = 'pain-lsp';
                    }
                }
            } else {
                // No workspace open, use PATH fallback
                lspPath = 'pain-lsp';
            }
        }

        // Server options - run LSP server
        const serverOptions: ServerOptions = {
            run: { command: lspPath, transport: TransportKind.stdio },
            debug: { command: lspPath, transport: TransportKind.stdio }
        };

        // Client options
        const clientOptions: LanguageClientOptions = {
            documentSelector: [{ scheme: 'file', language: 'pain' }],
            synchronize: {
                // Only create file watcher if workspace is available
                fileEvents: workspaceFolders && workspaceFolders.length > 0
                    ? vscode.workspace.createFileSystemWatcher('**/.pain')
                    : undefined
            }
        };

        // Register format document command
        const formatCommand = vscode.commands.registerCommand('pain.formatDocument', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor || editor.document.languageId !== 'pain') {
                return;
            }

            const document = editor.document;
            const text = document.getText();
            
            // Find pain-compiler executable
            let compilerPath = '';
            if (workspaceFolders && workspaceFolders.length > 0) {
                const workspaceRoot = workspaceFolders[0].uri.fsPath;
                const devPath = path.join(workspaceRoot, 'target', 'debug', 'pain-compiler');
                const devPathExe = devPath + (process.platform === 'win32' ? '.exe' : '');
                if (fs.existsSync(devPathExe)) {
                    compilerPath = devPathExe;
                } else {
                    const releasePath = path.join(workspaceRoot, 'target', 'release', 'pain-compiler');
                    const releasePathExe = releasePath + (process.platform === 'win32' ? '.exe' : '');
                    if (fs.existsSync(releasePathExe)) {
                        compilerPath = releasePathExe;
                    } else {
                        compilerPath = 'pain-compiler';
                    }
                }
            } else {
                compilerPath = 'pain-compiler';
            }

            // Create temporary file for formatting
            const tempFile = path.join(path.dirname(document.uri.fsPath), '.pain_format_temp.pain');
            try {
                fs.writeFileSync(tempFile, text);
                
                // Run formatter
                const command = `"${compilerPath}" format --input "${tempFile}" --stdout`;
                
                exec(command, (error: any, stdout: string, stderr: string) => {
                    if (error) {
                        vscode.window.showErrorMessage(`Formatting failed: ${error.message}`);
                        return;
                    }
                    
                    if (stderr) {
                        vscode.window.showWarningMessage(`Formatting warning: ${stderr}`);
                    }
                    
                    // Apply formatted text
                    const edit = new vscode.WorkspaceEdit();
                    const fullRange = new vscode.Range(
                        document.positionAt(0),
                        document.positionAt(text.length)
                    );
                    edit.replace(document.uri, fullRange, stdout);
                    vscode.workspace.applyEdit(edit);
                });
            } catch (error: any) {
                vscode.window.showErrorMessage(`Formatting failed: ${error.message}`);
            } finally {
                // Clean up temp file
                if (fs.existsSync(tempFile)) {
                    fs.unlinkSync(tempFile);
                }
            }
        });

        context.subscriptions.push(formatCommand);

        // Create and start the client
        try {
            client = new LanguageClient(
                'painLanguageServer',
                'Pain Language Server',
                serverOptions,
                clientOptions
            );

            client.start().catch((error) => {
                console.error('Failed to start Pain Language Server:', error);
                const errorMessage = error instanceof Error ? error.message : String(error);
                // Don't show error for NoWorkspaceUriError if no workspace is open (expected behavior)
                if (!errorMessage.includes('NoWorkspaceUriError') || (workspaceFolders && workspaceFolders.length > 0)) {
                    vscode.window.showErrorMessage(`Failed to start Pain Language Server: ${errorMessage}`);
                }
            });
        } catch (error) {
            console.error('Failed to create Language Client:', error);
            const errorMessage = error instanceof Error ? error.message : String(error);
            // Don't show error for NoWorkspaceUriError if no workspace is open (expected behavior)
            if (!errorMessage.includes('NoWorkspaceUriError') || (workspaceFolders && workspaceFolders.length > 0)) {
                vscode.window.showErrorMessage(`Failed to create Language Client: ${errorMessage}`);
            }
        }
    } catch (error) {
        console.error('Error activating Pain extension:', error);
        vscode.window.showErrorMessage(`Error activating Pain extension: ${error instanceof Error ? error.message : String(error)}`);
    }
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}

