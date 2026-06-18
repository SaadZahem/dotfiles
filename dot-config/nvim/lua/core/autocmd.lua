-- Automatically compile SILE documents on save (Asynchronous)
vim.api.nvim_create_autocmd('BufWritePost', {
  pattern = '*.sil',
  group = vim.api.nvim_create_augroup('SileCompile', { clear = true }),
  callback = function()
    local dir = vim.fn.shellescape(vim.fn.expand '%:p:h')
    local file = vim.fn.shellescape(vim.fn.expand '%:t')

    local cmd = 'cd ' .. dir .. ' && env -u LUA_PATH -u LUA_CPATH -u LUA_INIT sile ' .. file

    -- Run the command asynchronously in the background
    vim.system({ 'sh', '-c', cmd }, { text = true }, function(result)
      -- CRITICAL: Background threads cannot directly update Neovim's UI.
      -- We must wrap UI updates inside vim.schedule() to push them back to the main thread.
      vim.schedule(function()
        if result.code ~= 0 then
          -- Combine standard error and standard output to ensure we catch the failure message
          local error_msg = (result.stderr ~= '' and result.stderr or result.stdout)
          vim.notify('SILE Compilation Failed:\n' .. error_msg, vim.log.levels.ERROR)
        else
          print 'SILE compiled successfully.'
        end
      end)
    end)
  end,
})
