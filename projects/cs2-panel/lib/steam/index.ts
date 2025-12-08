import { SteamManager } from './steamManager';
import { SteamAPI, SteamLoginOptions, SteamUserStatus } from './steamAPI';

// Создаем глобальный экземпляр SteamManager
const steamManager = new SteamManager();

export { steamManager, SteamManager, SteamAPI };
export type { SteamLoginOptions, SteamUserStatus }; 