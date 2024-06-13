" Vim syntax file
" Language: Bloom
" Maintainer: Nauhan Alves
" Latest Revision: 06 january 2024

if exists('b:current_syntax')
    finish
endif

syntax match simpleVar "\k\+" nextgroup=simpleAssignment
syntax match simpleAssignment "=" contained nextgroup=simpleValue
syntax match simpleValue ".*" contained

hi def link simpleVar Identifier
hi def link simpleAssignment Statement
hi def link simpleValue String

let b:current_syntax = 'bloom'

