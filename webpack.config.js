const webpack = require("webpack");
const autoprefixer = require('autoprefixer');
const path = require('path');

function tryResolve_(url, sourceFilename) {
  // Put require.resolve in a try/catch to avoid node-sass failing with cryptic libsass errors
  // when the importer throws
  try {
    return require.resolve(url, {paths: [path.dirname(sourceFilename)]});
  } catch (e) {
    return '';
  }
}

function tryResolveScss(url, sourceFilename) {
  // Support omission of .scss and leading _
  const normalizedUrl = url.endsWith('.scss') ? url : `${url}.scss`;
  return tryResolve_(normalizedUrl, sourceFilename) ||
    tryResolve_(path.join(path.dirname(normalizedUrl), `_${path.basename(normalizedUrl)}`),
      sourceFilename);
}

function materialImporter(url, prev) {
  if (url.startsWith('@material')) {
    const resolved = tryResolveScss(url, prev);
    return {file: resolved || url};
  }
  return {file: url};
}

/**
Given a string `name`, returns a rule to bundle
RegExp(`${name}\.scss$`) to `biz-portal.bundle.${name}.css`
**/
function themeBundle(name) {
  return {
    test: new RegExp(`${name}\.scss$`),
    use: [
      {
        loader: 'file-loader',
        options: {
          name: `biz-portal.bundle.${name}.css`,
        },
      },
      {loader: 'extract-loader'},
      {loader: 'css-loader'},
      {
        loader: 'postcss-loader',
        options: {
          plugins: () => [autoprefixer()]
        }
      },
      {
        loader: 'sass-loader',
        options: {
          importer: materialImporter
        },
      }
    ],
  }
}

module.exports = {
  context: __dirname,
  entry: [
    // Entry for each theme
    './assets/scss/biz-portal-default.scss',
    './assets/scss/biz-portal-WC033.scss',
    './assets/js/html5-details-polyfill.js',
    './assets/js/biz-portal.js'
  ],
  output: {
    filename: 'biz-portal.bundle.js',
    path: path.resolve('./assets/bundles'),
  },
  resolve: {
    alias: {
      jquery: "jquery/src/jquery"
    }
  },
  plugins: [
    new webpack.ProvidePlugin({ jQuery: 'jquery', $: 'jquery', "window.jQuery": "jquery" }),
  ],

  module: {
    rules: [
      // Rule for each theme
      themeBundle("WC033"),
      themeBundle("default"),

      {
        test: /\.js$/,
        loader: 'babel-loader',
        query: {
          presets: ['@babel/preset-env'],
        },
      }
    ],
  },
  devtool: 'source-map',
};
