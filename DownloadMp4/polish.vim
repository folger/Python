"http:\/\/www.tudou.com[^"]\{-}">第\d\+集
function! PolishTudou()
  silent! %s/<//g
  silent! %s/">/ /g
  silent! %s/第\(\d\+\)集/\1/g
  silent! %s/tudou\zs/xia/g
endfunction
command! Tudou call PolishTudou()

"http:\/\/v.pps.tv[^"]\{-}" title="第&nbsp;\d\+&nbsp;集
function! PolishPPS()
  silent! %s/">//g
  silent! %s/#from_splay" title="第&nbsp;\(\d\+\)&nbsp;集//g
endfunction
command! PPS call PolishPPS()

"http:\/\/tv.sohu.com\/\d\+\/n\d\+.shtml">第\d\+集
function! PolishSohu()
  silent! %s/<//g
  silent! %s/">/ /g
  silent! %s/第\(\d\+\)集/\1/g
  silent! %s/sohu\zs/xia/g
endfunction
command! Sohu call PolishSohu()

"http:\/\/k.youku.com\/[^"]\{-}\/flv\/[^"]\{-}"
"n"Byf"
