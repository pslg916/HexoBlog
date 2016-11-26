---
title: MathJax Support for Hexo
date: 2016-11-26 18:57:40
tags: Hexo
categories: 工具
---

-------------------------------------

#  Install

```shell
npm install hexo-math --save
```

-------------------------------------

#  Config

In your site's _config.yml:

```
# MathJax
math:
  engine: 'mathjax' # or 'katex'
  mathjax:
    src: "//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"
    config:
      tex2jax:
        inlineMath: [ ['$','$'], ["\\(","\\)"] ]
        skipTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
        processEscapes: true
        TeX:
          equationNumbers:
          autoNumber: "AMS"
```

-------------------------------------

# Usage

MathJax basic tutorial and quick reference.
http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference
