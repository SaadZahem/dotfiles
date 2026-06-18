-- Set leader key
vim.g.mapleader = ' '
vim.g.maplocalleader = '\\'

-- Disable the spacebar key's default behavior in Normal and Visual modes
vim.keymap.set({ 'n', 'v' }, '<Space>', '<Nop>', { silent = true })

-- Quickly exit insert mode
vim.keymap.set('i', 'jk', '<Esc>')

-- For conciseness
local opts = { noremap = true, silent = true }
local function cmd(command)
  return '<cmd>' .. command .. '<CR>'
end

-- save file
vim.keymap.set('n', '<C-s>', cmd 'w', opts)

-- save file without auto-formatting
vim.keymap.set('n', '<leader>sn', cmd 'noautocmd w', opts)

-- quit file
vim.keymap.set('n', '<C-q>', cmd 'q', opts)

-- delete single character without copying into register
vim.keymap.set('n', 'x', '"_x', opts)

-- Vertical scroll and center
vim.keymap.set('n', '<C-d>', '<C-d>zz', opts)
vim.keymap.set('n', '<C-u>', '<C-u>zz', opts)

-- Find and center
vim.keymap.set('n', 'n', 'nzzzv', opts)
vim.keymap.set('n', 'N', 'Nzzzv', opts)

-- Resize with arrows
vim.keymap.set('n', '<Up>', cmd 'resize -2', opts)
vim.keymap.set('n', '<Down>', cmd 'resize +2', opts)
vim.keymap.set('n', '<Left>', cmd 'vertical resize -2', opts)
vim.keymap.set('n', '<Right>', cmd 'vertical resize +2', opts)

-- Buffers
vim.keymap.set('n', '<Tab>', cmd 'bnext', opts)
vim.keymap.set('n', '<S-Tab>', cmd 'bprevious', opts)
vim.keymap.set('n', '<leader>x', cmd 'bdelete!', opts) -- close buffer
vim.keymap.set('n', '<leader>b', cmd 'enew', opts) -- new buffer

-- Window management
vim.keymap.set('n', '<leader>v', '<C-w>v', opts) -- split window vertically
vim.keymap.set('n', '<leader>h', '<C-w>s', opts) -- split window horizontally
vim.keymap.set('n', '<leader>se', '<C-w>=', opts) -- make split windows equal width & height
vim.keymap.set('n', '<leader>xs', cmd 'close', opts) -- close current split window

-- Navigate between splits
vim.keymap.set('n', '<C-k>', cmd 'wincmd k', opts)
vim.keymap.set('n', '<C-j>', cmd 'wincmd j', opts)
vim.keymap.set('n', '<C-h>', cmd 'wincmd h', opts)
vim.keymap.set('n', '<C-l>', cmd 'wincmd l', opts)

-- Tabs
vim.keymap.set('n', '<leader>to', cmd 'tabnew', opts) -- open new tab
vim.keymap.set('n', '<leader>tx', cmd 'tabclose', opts) -- close current tab
vim.keymap.set('n', '<leader>tn', cmd 'tabn', opts) --  go to next tab
vim.keymap.set('n', '<leader>tp', cmd 'tabp', opts) --  go to previous tab

-- Toggle line wrapping
vim.keymap.set('n', '<leader>lw', cmd 'set wrap!', opts)

-- Stay in indent mode
vim.keymap.set('v', '<', '<gv', opts)
vim.keymap.set('v', '>', '>gv', opts)

-- Keep last yanked when pasting
vim.keymap.set('v', 'p', '"_dP', opts)

-- Diagnostic keymaps
vim.keymap.set('n', '[d', function()
  vim.diagnostic.jump { count = -1, float = true }
end, { desc = 'Go to previous diagnostic message' })

vim.keymap.set('n', ']d', function()
  vim.diagnostic.jump { count = 1, float = true }
end, { desc = 'Go to next diagnostic message' })

vim.keymap.set('n', '<leader>d', vim.diagnostic.open_float, { desc = 'Open floating diagnostic message' })
vim.keymap.set('n', '<leader>q', vim.diagnostic.setloclist, { desc = 'Open diagnostics list' })
