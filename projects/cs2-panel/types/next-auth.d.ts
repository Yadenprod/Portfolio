import NextAuth from "next-auth";
import { JWT } from "next-auth/jwt";

declare module "next-auth" {
  /**
   * Расширение стандартного типа User для Next Auth
   */
  interface User {
    id: string;
    name: string;
    email: string;
    role: string;
  }

  /**
   * Расширение стандартного типа Session для Next Auth
   */
  interface Session {
    user: {
      id: string;
      name: string;
      email: string;
      role: string;
    };
  }
}

declare module "next-auth/jwt" {
  /**
   * Расширение стандартного типа JWT для Next Auth
   */
  interface JWT {
    id: string;
    role: string;
  }
} 