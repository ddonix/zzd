set ai
set tabstop=4
au BufReadPost * if line("'\"") > 0|if line("'\"") <= line("$")|exe("norm '\"")|else|exe "norm $"|endif|endif
syntax on
colorscheme desert  
filetype on  
