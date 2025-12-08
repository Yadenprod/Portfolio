import postcssImport from 'postcss-import';
import tailwindcss from '@tailwindcss/postcss';
import autoprefixer from 'autoprefixer';
import postcssNesting from 'postcss-nesting';

export default {
  plugins: [
    postcssImport(),
    postcssNesting(),
    tailwindcss(),
    autoprefixer(),
  ],
};
