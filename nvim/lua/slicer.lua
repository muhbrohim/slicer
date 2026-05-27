-- slicer.lua — Neovim plugin
--
-- Thin wrapper around the `slice` CLI. Same keymap works in normal and visual
-- modes — in visual mode it slices the selection, in normal mode it slices
-- the current line.
--
--   <leader>ss   table (default)
--   <leader>sb   table + byte offsets   (--offsets)
--   <leader>sj   json                   (--json)
--   <leader>sr   key=value lines        (--raw)
--   <leader>sS   open the spec matching a service code (CA####, US####, AC####,
--                ANI####, …) on the current line (normal only)
--
-- Commands:
--
--   :SliceOpenSpec            open spec for code found on current line
--   :SliceOpenSpec CA1033     open spec for the given code (case-insensitive,
--                             leading '#' allowed)
--
-- Note: spec buffers (specs/body/*.spec) are opened with 'swapfile' disabled
-- to avoid recurring stale-swap prompts on these "peek" buffers. They open in
-- a right-hand vertical split; subsequent opens reuse the existing spec window.
--
-- Setup (in your init.lua):
--
--   vim.env.SLICER_HOME = "/path/to/slicer"   -- required for <leader>so
--   require("slicer").setup({
--     -- optional overrides
--     slice_cmd = "slice",                    -- path to the `slice` CLI
--     keymaps   = true,                       -- set false to skip default keymaps
--   })

local M = {}

local defaults = {
  slice_cmd = "slice",
  spec_cmd = "spec",
  keymaps = true,
}

local config = vim.deepcopy(defaults)
local cmd_ok = true

-- Exposed for sub-modules (e.g. slicer.telescope) so they can read user config.
M._config = config

-- ---------------------------------------------------------------------------
-- helpers
-- ---------------------------------------------------------------------------

local function notify(msg, level)
  vim.notify("[slicer] " .. msg, level or vim.log.levels.INFO)
end

local function validate_cmd()
  -- Skip validation for multi-word commands (e.g. "python -m slicer");
  -- vim.fn.executable can't handle them and the user clearly knows what they want.
  if config.slice_cmd:find("%s") then
    cmd_ok = true
    return true
  end
  if vim.fn.executable(config.slice_cmd) == 1 then
    cmd_ok = true
    return true
  end
  cmd_ok = false
  notify(
    ("slice_cmd not executable: %s\nCheck your config or recreate the venv."):format(config.slice_cmd),
    vim.log.levels.ERROR
  )
  return false
end

-- Map slicer output format -> CLI flag and Neovim filetype for the output buffer.
local FORMATS = {
  table   = { flag = nil,         filetype = "slicer-output" },
  offsets = { flag = "--offsets", filetype = "slicer-output" },
  json    = { flag = "--json",    filetype = "json" },
  raw     = { flag = "--raw",     filetype = "slicer-output" },
}

local function open_output(text, filetype)
  vim.cmd("rightbelow vsplit")
  local buf = vim.api.nvim_create_buf(false, true)
  vim.api.nvim_win_set_buf(0, buf)
  vim.api.nvim_buf_set_lines(buf, 0, -1, false, vim.split(text, "\n", { plain = true }))
  vim.bo[buf].buftype = "nofile"
  vim.bo[buf].bufhidden = "wipe"
  vim.bo[buf].swapfile = false
  vim.bo[buf].modifiable = false
  vim.bo[buf].filetype = filetype or "slicer-output"
end

local function run_slice(message, format)
  format = format or "table"
  local spec = FORMATS[format]
  if not spec then
    notify("unknown format: " .. tostring(format), vim.log.levels.ERROR)
    return
  end
  if not cmd_ok then
    notify("slice_cmd unavailable (" .. config.slice_cmd .. ")", vim.log.levels.ERROR)
    return
  end
  if not message or message == "" then
    notify("no message to slice", vim.log.levels.WARN)
    return
  end

  local cmd = { config.slice_cmd }
  if spec.flag then table.insert(cmd, spec.flag) end
  table.insert(cmd, message)
  local result = vim.system(cmd, { text = true }):wait()

  if result.code ~= 0 and (result.stdout == nil or result.stdout == "") then
    notify("slice failed: " .. (result.stderr or "unknown error"), vim.log.levels.ERROR)
    return
  end

  local output = result.stdout or ""
  if result.stderr and result.stderr ~= "" then
    output = output .. "\n--- stderr ---\n" .. result.stderr
  end
  open_output(output, spec.filetype)
end

local function get_visual_selection()
  -- Re-enter visual mode briefly to refresh `'<` / `'>`.
  local mode = vim.fn.mode()
  if mode == "v" or mode == "V" or mode == "" then
    vim.cmd('normal! "vy')
    return vim.fn.getreg("v")
  end
  -- Fallback: use the marks from the last visual selection.
  local s = vim.fn.getpos("'<")
  local e = vim.fn.getpos("'>")
  local lines = vim.api.nvim_buf_get_lines(0, s[2] - 1, e[2], false)
  if #lines == 0 then
    return ""
  end
  if #lines == 1 then
    return lines[1]:sub(s[3], e[3])
  end
  lines[1] = lines[1]:sub(s[3])
  lines[#lines] = lines[#lines]:sub(1, e[3])
  return table.concat(lines, "\n")
end

-- ---------------------------------------------------------------------------
-- commands
-- ---------------------------------------------------------------------------

function M.slice_line(format)
  run_slice(vim.api.nvim_get_current_line(), format)
end

function M.slice_selection(format)
  run_slice(get_visual_selection(), format)
end

-- Mode-aware: visual -> selection, else -> current line. Use this in keymaps
-- that you want bound the same way in both normal and visual modes.
function M.slice_smart(format)
  local mode = vim.fn.mode()
  if mode == "v" or mode == "V" or mode == "\22" then
    M.slice_selection(format)
  else
    M.slice_line(format)
  end
end

local function purge_swap_for(path)
  -- Best-effort: remove any stale .swp/.swo for the given file path.
  -- nvim's global swap dir encodes path separators as '%' but always
  -- preserves the basename verbatim at the tail, so a basename glob is
  -- both narrow and safe.
  pcall(function()
    local swapdir = vim.fn.stdpath("data") .. "/swap"
    local basename = vim.fs.basename(path)
    if not basename or basename == "" then return end
    for _, sf in ipairs(vim.fn.glob(swapdir .. "/*" .. basename .. ".sw?", true, true)) do
      vim.fn.delete(sf)
    end
  end)
end

function M.open_spec(code)
  local home = vim.env.SLICER_HOME
  if not home or home == "" then
    notify("SLICER_HOME is not set", vim.log.levels.ERROR)
    return
  end

  if code and code ~= "" then
    -- Normalize: strip leading '#', uppercase.
    code = code:gsub("^#", ""):upper()
  else
    local line = vim.api.nvim_get_current_line()
    -- Scan for [A-Z]+%d+ tokens, accept 2-4 letter prefix + 3-6 digits.
    for alpha, digits in line:gmatch("([A-Z]+)(%d+)") do
      if #alpha >= 2 and #alpha <= 4 and #digits >= 3 and #digits <= 6 then
        code = alpha .. digits
        break
      end
    end
    if not code then
      notify("no service code (e.g. CA1017, ANI4000) found on this line", vim.log.levels.WARN)
      return
    end
  end

  local body = vim.fs.joinpath(home, "specs", "body")
  local candidates = {
    vim.fs.joinpath(body, code .. ".spec"),
    vim.fs.joinpath(body, "#" .. code .. ".spec"),
  }
  for _, path in ipairs(candidates) do
    if vim.fn.filereadable(path) == 1 then
      -- Spec files are "peek" buffers; avoid the swap-exists prompt entirely.
      purge_swap_for(path)

      local abs = vim.fn.fnamemodify(path, ":p")
      local exact_win, spec_win
      -- Scan windows in this tab page:
      --   * exact_win -> already showing this exact spec
      --   * spec_win  -> showing some other specs/body/*.spec file (reuse target)
      for _, win in ipairs(vim.api.nvim_tabpage_list_wins(0)) do
        local name = vim.api.nvim_buf_get_name(vim.api.nvim_win_get_buf(win))
        if name == abs then
          exact_win = win
          break
        elseif not spec_win and name:match("[/\\]specs[/\\]body[/\\][^/\\]+%.spec$") then
          spec_win = win
        end
      end

      if exact_win then
        vim.api.nvim_set_current_win(exact_win)
      elseif spec_win then
        vim.api.nvim_set_current_win(spec_win)
        vim.cmd("edit " .. vim.fn.fnameescape(path))
      else
        vim.cmd("rightbelow vsplit " .. vim.fn.fnameescape(path))
      end

      vim.bo.swapfile = false
      pcall(function()
        local sw = vim.fn.swapname(0)
        if sw and sw ~= "" then vim.fn.delete(sw) end
      end)
      return
    end
  end
  notify(
    ("spec not found for %s. Tried:\n  %s\n  %s"):format(code, candidates[1], candidates[2]),
    vim.log.levels.WARN
  )
end

-- Back-compat shim for users who bound the old function directly.
function M.open_spec_under_cursor()
  M.open_spec()
end

-- ---------------------------------------------------------------------------
-- setup
-- ---------------------------------------------------------------------------

function M.setup(opts)
  config = vim.tbl_deep_extend("force", defaults, opts or {})
  M._config = config
  validate_cmd()

  -- Commands. The base names (SliceLine / SliceSelection) keep their existing
  -- behavior (default table); per-format variants are additive.
  local ucmd = vim.api.nvim_create_user_command
  ucmd("SliceLine",            function() M.slice_line() end,                   {})
  ucmd("SliceLineOffsets",     function() M.slice_line("offsets") end,          {})
  ucmd("SliceLineJson",        function() M.slice_line("json") end,             {})
  ucmd("SliceLineRaw",         function() M.slice_line("raw") end,              {})
  ucmd("SliceSelection",         function() M.slice_selection() end,            { range = true })
  ucmd("SliceSelectionOffsets",  function() M.slice_selection("offsets") end,   { range = true })
  ucmd("SliceSelectionJson",     function() M.slice_selection("json") end,      { range = true })
  ucmd("SliceSelectionRaw",      function() M.slice_selection("raw") end,       { range = true })
  ucmd("SliceOpenSpec", function(o)
    M.open_spec(o.args ~= "" and o.args or nil)
  end, { nargs = "?" })
  ucmd("SliceFindSpec", function()
    require("slicer.telescope").find_specs()
  end, { desc = "slicer: telescope picker for specs" })
  ucmd("SliceReloadSpecs", function()
    require("slicer.telescope").reload()
    notify("spec list cache cleared")
  end, {})

  -- Auto-register the telescope extension if telescope is available.
  pcall(function() require("telescope").load_extension("slicer") end)

  -- Disable swapfile for spec body files however they are opened (`:e`,
  -- telescope, netrw, …). BufReadPre fires before the swap check, which is
  -- what actually suppresses the "swap file already exists" prompt.
  local spec_group = vim.api.nvim_create_augroup("SlicerSpecNoSwap", { clear = true })
  local spec_patterns = { "*/specs/body/*.spec", "*\\specs\\body\\*.spec" }

  -- Disable swapfile for spec body files however they are opened.
  vim.api.nvim_create_autocmd({ "BufReadPre", "BufNewFile" }, {
    group = spec_group,
    pattern = spec_patterns,
    callback = function() vim.bo.swapfile = false end,
    desc = "slicer: disable swap for spec body files",
  })

  -- Suppress the "swap file already exists" prompt for spec body files by
  -- telling nvim to delete the stale swap and continue.
  vim.api.nvim_create_autocmd("SwapExists", {
    group = spec_group,
    pattern = spec_patterns,
    callback = function() vim.v.swapchoice = "e" end,
    desc = "slicer: auto-dismiss swap prompt for spec body files",
  })

  if config.keymaps then
    local map = vim.keymap.set
    local nx = { "n", "x" }
    -- Same key in normal and visual: in visual it slices the selection,
    -- in normal it slices the current line.
    map(nx, "<leader>ss", function() M.slice_smart() end,          { desc = "slicer: slice (table)" })
    map(nx, "<leader>sb", function() M.slice_smart("offsets") end, { desc = "slicer: slice (table+offsets)" })
    map(nx, "<leader>sj", function() M.slice_smart("json") end,    { desc = "slicer: slice (json)" })
    map(nx, "<leader>sr", function() M.slice_smart("raw") end,     { desc = "slicer: slice (raw)" })
    -- Spec opener (only meaningful in normal mode).
    map("n", "<leader>sS", M.open_spec_under_cursor, { desc = "slicer: open spec under cursor" })
    map("n", "<leader>sf", function() require("slicer.telescope").find_specs() end,
        { desc = "slicer: find spec (telescope)" })
  end
end

return M
