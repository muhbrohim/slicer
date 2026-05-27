-- Telescope extension registration: enables `:Telescope slicer specs`.
local has_telescope, telescope = pcall(require, "telescope")
if not has_telescope then
  return {}
end

return telescope.register_extension({
  exports = {
    specs = function(opts) require("slicer.telescope").find_specs(opts) end,
  },
})
