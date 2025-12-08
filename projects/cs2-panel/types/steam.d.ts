declare module 'steam-user' {
  import { EventEmitter } from 'events';

  class SteamUser extends EventEmitter {
    steamID: any;
    
    constructor(options?: any);
    
    logOn(options: {
      accountName: string;
      password: string;
      twoFactorCode?: string;
      rememberPassword?: boolean;
      logonID?: number;
      [key: string]: any;
    }): void;
    
    logOff(): void;
    
    gamesPlayed(appIds: number | number[]): void;
    
    getProductInfo(apps: number[], packages: number[], enablePics?: boolean): Promise<any>;
  }
  
  export = SteamUser;
}

declare module 'steam-totp' {
  export function generateAuthCode(secret: string, timeOffset?: number): string;
  
  export function generateConfirmationKey(identitySecret: string, time: number, tag: string): Buffer;
  
  export function getTimeOffset(callback: (error: Error | null, offset: number) => void): void;
  
  export function getTimeOffset(): Promise<number>;
  
  export function time(): number;
} 