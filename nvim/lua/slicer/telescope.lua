-- slicer/telescope.lua — fuzzy picker for spec files.
--
-- Lists all body specs with their endpoint, category, and service code,
-- pulled live from `spec list --json`. Selecting an entry opens the spec
-- via the existing `require("slicer").open_spec(code)` path (reuses window
-- management, swap-suppression, etc).
--
-- Works with or without telescope.nvim installed:
--   * if telescope is available -> rich picker with previewer
--   * otherwise                 -> falls back to vim.ui.select
--
-- Public API:
--   require("slicer.telescope").find_specs(opts)
--   require("slicer.telescope").reload()        -- clear cached spec list

local M = {}

local cache = nil  -- list of entries (cached for the session)

local function notify(msg, level)
  vim.notify("[slicer.telescope] " .. msg, level or vim.log.levels.INFO)
end

-- vim.json.decode returns vim.NIL (userdata) for JSON null, which is truthy
-- in Lua. Normalize to actual nil so `x or default` works as expected.
local function denil(v)
  if v == nil or v == vim.NIL then return nil end
  return v
end

local function get_spec_cmd()
  -- Allow override via the main slicer config.
  local ok, slicer = pcall(require, "slicer")
  if ok and slicer and slicer._config and slicer._config.spec_cmd then
    return slicer._config.spec_cmd
  end
  return "spec"
end

local function fetch_entries()
  if cache then return cache end

  local spec_cmd = get_spec_cmd()
  local cmd
  if spec_cmd:find("%s") then
    -- multi-word: split on whitespace
    cmd = {}
    for token in spec_cmd:gmatch("%S+") do table.insert(cmd, token) end
    table.insert(cmd, "list")
    table.insert(cmd, "--json")
  else
    cmd = { spec_cmd, "list", "--json" }
  end

  local result = vim.system(cmd, { text = true }):wait()
  if result.code ~= 0 then
    notify("`spec list --json` failed: " .. (result.stderr or "unknown"), vim.log.levels.ERROR)
    return nil
  end

  local ok, decoded = pcall(vim.json.decode, result.stdout or "")
  if not ok or type(decoded) ~= "table" then
    notify("could not parse spec list JSON", vim.log.levels.ERROR)
    return nil
  end

  cache = decoded
  return cache
end

function M.reload()
  cache = nil
end

local function format_display(entry)
  local code = denil(entry.service_code) or "?"
  local cat = denil(entry.category) or "-"
  local pgm = denil(entry.program) or "-"
  local ep = denil(entry.endpoint) or "<none>"
  return string.format("%-10s  %-4s  %-9s  %s", code, cat, pgm, ep)
end

local function open_entry(entry)
  if not entry or not entry.service_code then return end
  local ok, slicer = pcall(require, "slicer")
  if not ok then
    notify("slicer module not found", vim.log.levels.ERROR)
    return
  end
  slicer.open_spec(entry.service_code)
end

-- Fallback picker when telescope is not installed.
local function fallback_picker(entries)
  vim.ui.select(entries, {
    prompt = "Spec:",
    format_item = format_display,
  }, function(choice)
    if choice then open_entry(choice) end
  end)
end

function M.find_specs(opts)
  opts = opts or {}
  local entries = fetch_entries()
  if not entries or #entries == 0 then
    notify("no specs to show", vim.log.levels.WARN)
    return
  end

  local has_telescope, pickers = pcall(require, "telescope.pickers")
  if not has_telescope then
    fallback_picker(entries)
    return
  end

  local finders = require("telescope.finders")
  local conf = require("telescope.config").values
  local actions = require("telescope.actions")
  local action_state = require("telescope.actions.state")
  local previewers = require("telescope.previewers")
  local entry_display = require("telescope.pickers.entry_display")

  -- Fixed-width columns so rows always align regardless of devicons/match
  -- highlights. Using entry_display avoids the variable indentation we'd
  -- otherwise get from telescope auto-prepending file-type icons via `path`.
  local displayer = entry_display.create({
    separator = "  ",
    items = {
      { width = 10 },  -- service_code
      { width = 4 },   -- category
      { width = 9 },   -- program
      { remaining = true },  -- endpoint
    },
  })

  local function make_display(entry)
    local v = entry.value
    return displayer({
      denil(v.service_code) or "?",
      denil(v.category) or "-",
      denil(v.program) or "-",
      denil(v.endpoint) or "<none>",
    })
  end

  pickers.new(opts, {
    prompt_title = "Slicer specs",
    finder = finders.new_table({
      results = entries,
      entry_maker = function(entry)
        local ordinal = table.concat({
          denil(entry.service_code) or "",
          denil(entry.endpoint) or "",
          denil(entry.category) or "",
          denil(entry.section) or "",
          denil(entry.program) or "",
        }, " ")
        return {
          value = entry,
          display = make_display,
          ordinal = ordinal,
          -- `filename` (not `path`) is what `previewers.cat.new` reads;
          -- avoids triggering telescope's icon-prepending path display.
          filename = denil(entry.spec_path),
        }
      end,
    }),
    sorter = conf.generic_sorter(opts),
    previewer = previewers.cat.new(opts),
    attach_mappings = function(prompt_bufnr, _)
      actions.select_default:replace(function()
        local selection = action_state.get_selected_entry()
        actions.close(prompt_bufnr)
        if selection then open_entry(selection.value) end
      end)
      return true
    end,
  }):find()
end

return M
