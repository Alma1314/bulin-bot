export {};

declare global {
  interface NovaBotDesktopAppUpdateCheckResult {
    ok: boolean;
    reason?: string | null;
    currentVersion?: string;
    latestVersion?: string | null;
    hasUpdate: boolean;
  }

  interface NovaBotDesktopAppUpdateResult {
    ok: boolean;
    reason?: string | null;
  }

  interface NovaBotAppUpdaterBridge {
    checkForAppUpdate: () => Promise<NovaBotDesktopAppUpdateCheckResult>;
    installAppUpdate: () => Promise<NovaBotDesktopAppUpdateResult>;
  }

  interface Window {
    nova-botAppUpdater?: NovaBotAppUpdaterBridge;
    nova-botDesktop?: {
      isDesktop: boolean;
      isDesktopRuntime: () => Promise<boolean>;
      getBackendState: () => Promise<{
        running: boolean;
        spawning: boolean;
        restarting: boolean;
        canManage: boolean;
      }>;
      restartBackend: (authToken?: string | null) => Promise<{
        ok: boolean;
        reason: string | null;
      }>;
      stopBackend: () => Promise<{
        ok: boolean;
        reason: string | null;
      }>;
      onTrayRestartBackend?: (callback: () => void) => () => void;
    };
  }
}
