module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    "plugin:vue/recommended",
    "eslint:recommended"
  ],
  parserOptions: {
    parser: "babel-eslint"
  },
  rules: {
    "no-console": process.env.NODE_ENV === "production" ? "warn" : "off",
    "no-debugger": process.env.NODE_ENV === "production" ? "warn" : "off",
    "no-multi-spaces": "error",
    "block-spacing": ["error", "always"],
    "space-before-function-paren": "error",
    "semi": ["error", "never"],
    "brace-style": ["error", "1tbs", { allowSingleLine: true }],
    "no-multiple-empty-lines": ["error", { max: 1 }],
    "no-trailing-spaces": "error",
    "indent": ["error", 2],
    "padded-blocks": ["error", "never"],
    "quote-props": ["error", "consistent-as-needed"],
    "quotes": ["error", "double"]
  }
}
