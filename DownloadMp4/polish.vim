"http:\/\/www.tudou.com[^"]\{-}">第\d\+集
function! PolishTudou()
  %s/<//g
  %s/">/ /g
  %s/第\(\d\+\)集/\1/g
  %s/tudou\zs/xia/g
endfunction
command! Tudou call PolishTudou()

"http:\/\/v.pps.tv[^"]\{-}" title="第&nbsp;\d\+&nbsp;集
function! PolishPPS()
  %s/">//g
  %s/#from_splay" title="第&nbsp;\(\d\+\)&nbsp;集//g
endfunction
command! PPS call PolishPPS()
