-- slicer.lua — Neovim plugin
--
-- Thin wrapper around the `slice` CLI. Three keymaps:
--   <leader>sp   slice current line
--   <leader>ss   slice visual selection
--   <leader>so   open the spec matching CA#### on the current line
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
  keymaps = true,
}

local config = vim.deepcopy(defaults)
local cmd_ok = true

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

local function open_output(text)
  vim.cmd("rightbelow vsplit")
  local buf = vim.api.nvim_create_buf(false, true)
  vim.api.nvim_win_set_buf(0, buf)
  vim.api.nvim_buf_set_lines(buf, 0, -1, false, vim.split(text, "\n", { plain = true }))
  vim.bo[buf].buftype = "nofile"
  vim.bo[buf].bufhidden = "wipe"
  vim.bo[buf].swapfile = false
  vim.bo[buf].modifiable = false
  vim.bo[buf].filetype = "slicer-output"
end

local function run_slice(message)
  if not cmd_ok then
    notify("slice_cmd unavailable (" .. config.slice_cmd .. ")", vim.log.levels.ERROR)
    return
  end
  if not message or message == "" then
    notify("no message to slice", vim.log.levels.WARN)
    return
  end

  local cmd = { config.slice_cmd, message }
  local result = vim.system(cmd, { text = true }):wait()

  if result.code ~= 0 and (result.stdout == nil or result.stdout == "") then
    notify("slice failed: " .. (result.stderr or "unknown error"), vim.log.levels.ERROR)
    return
  end

  local output = result.stdout or ""
  if result.stderr and result.stderr ~= "" then
    output = output .. "\n--- stderr ---\n" .. result.stderr
  end
  open_output(output)
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

function M.slice_line()
  run_slice(vim.api.nvim_get_current_line())
end

function M.slice_selection()
  run_slice(get_visual_selection())
end

function M.open_spec_under_cursor()
  local home = vim.env.SLICER_HOME
  if not home or home == "" then
    notify("SLICER_HOME is not set", vim.log.levels.ERROR)
    return
  end
  local line = vim.api.nvim_get_current_line()
  local code = line:match("[A-Z][A-Z]%d%d%d%d?%d?")
  if not code then
    notify("no service code (e.g. CA1017) found on this line", vim.log.levels.WARN)
    return
  end
  local path = home .. "/specs/body/" .. code .. ".spec"
  if vim.fn.filereadable(path) == 0 then
    notify("spec not found: " .. path, vim.log.levels.WARN)
    return
  end
  vim.cmd("edit " .. vim.fn.fnameescape(path))
end

-- ---------------------------------------------------------------------------
-- setup
-- ---------------------------------------------------------------------------

function M.setup(opts)
  config = vim.tbl_deep_extend("force", defaults, opts or {})
  validate_cmd()

  vim.api.nvim_create_user_command("SliceLine", M.slice_line, {})
  vim.api.nvim_create_user_command("SliceSelection", M.slice_selection, { range = true })
  vim.api.nvim_create_user_command("SliceOpenSpec", M.open_spec_under_cursor, {})

  if config.keymaps then
    local map = vim.keymap.set
    map("n", "<leader>sp", M.slice_line, { desc = "slicer: slice current line" })
    map("x", "<leader>ss", M.slice_selection, { desc = "slicer: slice visual selection" })
    map("n", "<leader>so", M.open_spec_under_cursor, { desc = "slicer: open spec under cursor" })
  end
end

return M
