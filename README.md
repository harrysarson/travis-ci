# Elm support on Travis-CI

This repo contains information and scripts to assist in maintenance and debugging of Elm support for [Travis-CI](https://travis-ci.org).

The original PR to add Elm support to Travis-CI is [travis-ci/travis-ci#934](https://github.com/travis-ci/travis-build/pull/934).  Part of the process of getting Elm support approved is to have a group of at least three people willing to provide support for travis issues related to the language plugin.  The current maintainers are listed at [elm-community/Manifesto/maintainers.md](https://github.com/elm-community/Manifesto/blob/master/maintainers.md).

You may report issues about Elm support on Travis-CI on this repo.

## Example configurations

| Name               | Working                                                                                                                                                             | Configuration                                                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Minimal            | [![Build Status](https://travis-ci.com/harrysarson/travis-ci.svg?branch=example-ci%2Fminimal-app)](https://travis-ci.com/harrysarson/travis-ci/branches)            | <script src="https://gist-it.appspot.com/github/harrysarson/travis-ci/blob/example-ci/minimal-app/.travis.yml"></script>            |
| 0.19.0             | [![Build Status](https://travis-ci.com/harrysarson/travis-ci.svg?branch=example-ci%2Fminimal-app-elm-0.19.0)](https://travis-ci.com/harrysarson/travis-ci/branches) | <script src="https://gist-it.appspot.com/github/harrysarson/travis-ci/blob/example-ci/minimal-app-elm-0.19.0/.travis.yml"></script> |
| 0.19.0 using array | [![Build Status](https://travis-ci.com/harrysarson/travis-ci.svg?branch=example-ci%2Fminimal-app-elm-0.19.0-array)](https://travis-ci.com/harrysarson/travis-ci/branches) | <script src="https://gist-it.appspot.com/github/harrysarson/travis-ci/blob/example-ci/minimal-app-elm-0.19.0-array/.travis.yml"></script> |
| 0.19.1             | [![Build Status](https://travis-ci.com/harrysarson/travis-ci.svg?branch=example-ci%2Fminimal-app-elm-0.19.1)](https://travis-ci.com/harrysarson/travis-ci/branches) | <script src="https://gist-it.appspot.com/github/harrysarson/travis-ci/blob/example-ci/minimal-app-elm-0.19.1/.travis.yml"></script> |
