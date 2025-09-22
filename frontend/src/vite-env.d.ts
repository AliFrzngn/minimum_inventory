/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  // more env variables...
}

// eslint-disable-next-line no-redeclare
interface ImportMeta {
  readonly env: ImportMetaEnv
}
