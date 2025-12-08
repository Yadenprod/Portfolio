import { ReactNode } from 'react';

// Добавляем объявление модуля для next/head
declare module 'next/head' {
  export default function Head({ children }: { children: ReactNode }): JSX.Element;
} 