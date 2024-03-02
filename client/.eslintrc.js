// .eslintrc.js

module.exports = {
    parser: 'babel-eslint', // Use babel-eslint parser for parsing JavaScript files
    extends: ['eslint:recommended', 'plugin:react/recommended'],
    plugins: ['react', 'react-hooks'],
    rules: {
      'react-hooks/rules-of-hooks': 'error', // Checks rules of Hooks
      'react-hooks/exhaustive-deps': 'warn', // Checks effect dependencies
    },
    settings: {
      react: {
        version: 'detect', // Automatically detect React version
      },
    },
  };
  