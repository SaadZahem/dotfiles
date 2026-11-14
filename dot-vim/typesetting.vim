function! s:SyncPdf () abort
  let l:pdf = get(b:, 'syncpdf', get(g:, 'syncpdf', expand('%:r') . '.pdf'))
  if !filereadable(l:pdf)
    echohl WarningMsg | echomsg 'SyncTeX: no such PDF: ' . l:pdf | echohl None
    return
  endif
  let l:input = expand('%:t')
  let l:arg = printf('%d:%d:%s %s',
        \ line('.'), col('.'), shellescape(l:input), shellescape(l:pdf))
  let l:out = system('zathura --synctex-forward ' . l:arg)
  if v:shell_error != 0
    echohl WarningMsg
    echomsg 'SyncTeX: forward search failed (is Zathura running?)' . (empty(l:out) ? '' : "\n" . l:out)
    echohl None
  endif
endfunction

nnoremap <silent> <F5> :<C-u>call <SID>SyncPdf()<CR>


function! s:CompileSile () abort
  let l:dir = expand('%:p:h')
  let l:file = expand('%:t')
  let l:sile = empty($SILE_BIN) ? 'sile' : $SILE_BIN
  let l:cmd = printf('cd %s && env -u LUA_PATH -u LUA_CPATH -u LUA_INIT SILE=%s sil-sync.sh --synctex %s',
        \ shellescape(l:dir), shellescape(l:sile), shellescape(l:file))
  let l:output = system(l:cmd)
  if v:shell_error != 0
    echo "SILE compilation failed:\n" . l:output
  elseif !empty(l:output)
    echo substitute(l:output, '\n\+$', '', '')
  endif
endfunction

augroup SileCompile
  autocmd!
  autocmd BufWritePost *.sil call s:CompileSile()
augroup END
