do
local _ENV = _ENV
package.preload[ "src.csv" ] = function( ... ) local arg = _G.arg;
local Writer = {}
function Writer:new(fields)
  self.__index = self
  return setmetatable({
    header = table.concat(fields, ','),
    columns = #fields,
    data = "",
  }, self)
end

local function quoted(string)
  return '"' .. tostring(string):gsub('"', '""') .. '"'
end

function Writer:record(fields)
  -- Create CSV record.
  local record = quoted(fields[1])
  for i = 2, self.columns do
    if not fields[i] then
      record = record .. ','
    else
      record = record .. ',' .. quoted(fields[i])
    end
  end
  return record
end

function Writer:write(fields)
  self.data = string.format("%s%s\n", self.data, self:record(fields))
end

return {Writer = Writer}
end
end

do
local _ENV = _ENV
package.preload[ "src.filters" ] = function( ... ) local arg = _G.arg;
-- Pandoc filters.

local pandoc = require "pandoc"
local log = require "src.log"
local utils = require "src.utils"

local function preprocess()
  -- Create filter that preprocesses headers by setting the filename
  -- attribute of Headers to the name of the file.

  local function Pandoc(doc)
    local filename
    for _, elem in ipairs(doc.blocks) do
      if elem.tag == "CodeBlock" then
        filename = utils.parse_filename(elem.text) or filename
      elseif elem.tag == "Header" and elem.level == 1 then
        assert(filename)
        elem.attributes.filename = filename
      end
    end
    return doc
  end

  return {
    Pandoc = Pandoc,
  }
end

local function init(slipbox)
  -- Create filter that preprocesses headers by splitting the document
  -- into sections.

  local function CodeBlock(elem)
      -- Strip slipbox-metadata code block.
      if utils.parse_filename(elem.text) then
        return {}
      end
  end

  local function Header(elem)
    -- Only scan level 1 headers.
    if elem.level ~= 1 then return end

    local id
    local content = elem.content
    if content[1].tag == "Str" then
      id = tonumber(content[1].text:match '^%d+$')
    end
    if id == nil then return end

    table.remove(content, 1)
    while #content > 0 do
      if content[1].tag == "Space" then
        table.remove(content, 1)
      else
        break
      end
    end
    local title = pandoc.utils.stringify(content)
    if not title or title == "" then return end

    local filename = elem.attributes.filename
    local err = slipbox:save_note(id, title, filename)
    if err then log.warning(err) end

    elem.identifier = id
    elem.attributes.title = title
    elem.attributes.level = elem.level  -- Gets added to parent section
    return elem
  end

  local function Pandoc(doc)
    doc.blocks = pandoc.utils.make_sections(false, nil, doc.blocks)
    return doc
  end

  return {
    Header = Header,
    CodeBlock = CodeBlock,
    Pandoc = Pandoc,
  }
end

local Collector = {}
function Collector:new(slipbox, div)
  local id = tonumber(div.identifier)
  if not id then return end

  self.__index = self
  return setmetatable({
    slipbox = slipbox,
    id = id,
    div = div,
    current_tag = nil,
    has_empty_link_target = false,
  }, self)
end

function Collector:Cite(elem)
  for _, citation in pairs(elem.citations) do
    self.slipbox:save_citation(self.id, "ref-" .. citation.id)
  end
end

function Collector:Image(elem)
  self.slipbox:save_image(self.id, elem.src)
end

function Collector:Link(elem)
  if not elem.target or elem.target == "" then
    self.has_empty_link_target = true
  end
  local link = utils.get_link(self.id, elem)
  if link then
    link.tag = self.current_tag
    self.slipbox:save_link(link)
  end
end

function Collector:Str(elem)
  local tag = utils.hashtag_prefix(elem.text)
  if tag then
    self.slipbox:save_link { src = self.id, dest = self.id, tag = tag }
    self.current_tag = tag
  end
end

function Collector:filter()
  return {
    Cite = function(elem) return self:Cite(elem) end,
    Image = function (elem) return self:Image(elem) end,
    Link = function(elem) return self:Link(elem) end,
    Str = function(elem) return self:Str(elem) end,
  }
end

local function collect(slipbox)
  -- Create filter that saves citations, links and tags.
  return {
    Div = function(div)
      local col = Collector:new(slipbox, div)
      if col then
        pandoc.walk_block(div, col:filter())
        if col.has_empty_link_target then
          slipbox.invalid.has_empty_link_target[col.id] = true
        end
      end
    end
  }
end

local function hashtag()
  -- Create filter that turns #tags into links.
  return {
    Str = function(elem)
      local tag = utils.hashtag_prefix(elem.text)
      if tag then
        return {
          pandoc.Link({pandoc.Str(tag)}, '#tags/' .. tag:sub(2)),
          pandoc.Str(elem.text:sub(#tag + 1)),
        }
      end
    end
  }
end

local Modifier = {}
function Modifier:new()
  self.__index = self
  return setmetatable({
    footnotes = {},
  }, self)
end

function Modifier.Link(elem)
  -- Rewrite links with empty targets/text.
  if not elem.target or elem.target == "" then
    return elem.content
  end

  local content = pandoc.utils.stringify(elem.content or "")
  if content == "" then
    return {
      pandoc.Str " [",
      pandoc.Link(
        {pandoc.Str(elem.target)},
        elem.target,
        elem.title),
      pandoc.Str "]",
    }
  end
end

function Modifier:Note(elem)
  -- Collect footnotes.
  table.insert(self.footnotes, pandoc.Div(elem.content))
  local count = #self.footnotes
  return pandoc.Superscript(pandoc.Str(tostring(count)))
end

function Modifier:filter()
  return {
    Link = function(elem) return self.Link(elem) end,
    Note = function(elem) return self:Note(elem) end,
  }
end

local function modify()
  -- Create filter that modifies the document.
  return {
    Div = function(div)
      local mod = Modifier:new()
      div = pandoc.walk_block(div, mod:filter())
      if next(mod.footnotes) then
        local ol = pandoc.OrderedList{}
        for _, block in ipairs(mod.footnotes) do
          table.insert(ol.content, {block})
        end
        table.insert(div.content, pandoc.HorizontalRule())
        table.insert(div.content, ol)
      end

      if div.attributes.level then
        if div.attributes.level == "1" then
          table.insert(div.classes, "slipbox-note")
        end
        div.attributes.level = nil
      end
      return div
    end
  }
end

local function citations(slipbox)
  return {
    Div = function(div)
      -- Suppress bibliography and update SQL.
      if div.identifier == "refs" then

        local function Div(elem)
          -- Save reference text.
          if utils.is_reference_id(elem.identifier) then
            slipbox:save_reference(elem.identifier, pandoc.utils.stringify(elem.content))
            return {}
          end
        end

        pandoc.walk_block(div, {Div = Div})
        return {}
      end
    end
  }
end

local function serialize(slipbox)
  -- Create filter to dump slipbox data into working directory.
  return {
    Pandoc = function()
      slipbox:write_data()
    end
  }
end

local function check(slipbox)
  -- Create filter that prints warning messages for invalid notes.
  return {
    Pandoc = function()
      local has_empty_link_target = {}
      for id in pairs(slipbox.invalid.has_empty_link_target) do
        table.insert(has_empty_link_target, id)
      end
      if #has_empty_link_target == 0 then
        return
      end

      table.sort(has_empty_link_target)

      local messages = {"The notes below contain links with an empty target."}
      local template = "%d. %s in '%s'."
      for _, id in ipairs(has_empty_link_target) do
        local note = slipbox.notes[id] or {}
        local title = note.title
        local filename = note.filename
        if title and filename then
          local message = template:format(id, title, filename)
          table.insert(messages, message)
        end
      end
      log.warning(messages)
    end
  }
end

local function cleanup()
  -- TODO only cleanup note section headers?
  return {
    Header = function(elem)
      elem.attributes = {}
      return elem
    end
  }
end

return {
  preprocess = preprocess,
  init = init,
  collect = collect,
  hashtag = hashtag,
  modify = modify,
  citations = citations,
  serialize = serialize,
  check = check,
  cleanup = cleanup,
}
end
end

do
local _ENV = _ENV
package.preload[ "src.log" ] = function( ... ) local arg = _G.arg;
-- Print errors.

local function show(messages)
  if not messages or #messages < 1 then return end
  io.stderr:write(messages[1])
  io.stderr:write '\n'
  for i = 2, #messages do
    io.stderr:write "  "
    io.stderr:write(messages[i])
    io.stderr:write '\n'
  end
end

local function warning(messages)
  io.stderr:write "[WARNING] "
  show(messages)
end

local function _error(messages)
  io.stderr:write "[ERROR] "
  show(messages)
end

return {
  warning = warning,
  error = _error,
}
end
end

do
local _ENV = _ENV
package.preload[ "src.slipbox" ] = function( ... ) local arg = _G.arg;
local csv = require "src.csv"
local utils = require "src.utils"

local SlipBox = {}
function SlipBox:new()
  self.__index = self
  return setmetatable({
    notes = {},
    links = {},
    citations = {},
    images = {},
    bibliography = {},
    invalid = {
      has_empty_link_target = {},
    },
  }, self)
end

function SlipBox:save_citation(id, citation)
  -- Save citation from note id (number).
  assert(type(id) == "number")
  local citations = self.citations[id] or {}
  citations[citation] = true
  self.citations[id] = citations
end

function SlipBox:save_image(id, filename)
  assert(type(id) == "number")
  assert(type(filename) == "string")

  local image = self.images[filename] or {
    id = id,
    filename = filename,
    notes = {},
  }
  self.images[filename] = image
  image.notes[id] = true
end

function SlipBox:save_reference(id, text)
  -- Save reference into slipbox.
  assert(type(id) == "string")
  assert(type(text) == "string")
  assert(id ~= "")
  assert(string ~= "")
  self.bibliography[id] = text
end

function SlipBox:save_note(id, title, filename)
  -- Save note into slipbox.
  -- Return list of error messages if a note with the same ID already
  -- exists.
  assert(type(id) == "number")
  assert(type(title) == "string")
  assert(type(filename) == "string")
  assert(title ~= "")
  assert(filename ~= "")

  local note = self.notes[id]
  if note then
    return {
      string.format("Duplicate ID: %d.", id),
      string.format("Could not insert note '%s'.", title),
      string.format("Note '%s' already uses the ID.", note.title)
    }
  end
  self.notes[id] = {title = title, filename = filename}
end

function SlipBox:save_link(link)
  if link and link.src then
    local links = self.links[link.src] or {}
    table.insert(links, link)
    self.links[link.src] = links
  end
end

local function notes_to_csv(notes)
  -- Generate CSV data from slipbox notes.
  local w = csv.Writer:new{"id", "title", "filename"}
  for id, note in pairs(notes) do
    if note.filename then
      w:write{id, note.title, note.filename}
      -- TODO show warning if note.filename is nil
      -- This occurs when the title in the header contains other symbols
      -- (ex: links, references, equations, etc.).
    end
  end
  return w.data
end

local function links_to_csv(links)
  -- Create CSV data from direct links in slipbox.
  local w = csv.Writer:new{"src", "dest", "tag"}
  for src, dests in pairs(links) do
    for _, dest in ipairs(dests) do
      w:write{src, dest.dest, dest.tag}
    end
  end
  return w.data
end

local function bibliography_to_csv(refs)
  local w = csv.Writer:new{"key", "text"}
  for ref, text in pairs(refs) do
    w:write{ref, text}
  end
  return w.data
end

local function files_to_csv(notes)
  local unique_filenames = {}
  for _, note in pairs(notes) do
    unique_filenames[note.filename] = true
  end

  local w = csv.Writer:new{"filename"}
  for filename in pairs(unique_filenames) do
    w:write{filename}
  end
  return w.data
end

local function citations_to_csv(citations)
  local w = csv.Writer:new{"note", "reference"}
  for id, cites in pairs(citations) do
    for cite in pairs(cites) do
      w:write{id, cite}
    end
  end
  return w.data
end

local function images_to_csv(images)
  local w = csv.Writer:new{"filename"}
  for filename in pairs(images) do
    w:write{filename}
  end
  return w.data
end

local function image_links_to_csv(images)
  local w = csv.Writer:new{"note", "image"}
  for filename, image in pairs(images) do
    for note in pairs(image.notes) do
      w:write{note, filename}
    end
  end
  return w.data
end

function SlipBox:write_data()
  -- Create CSV data to files.
  local write = utils.write_text
  write("files.csv", files_to_csv(self.notes))
  write("notes.csv", notes_to_csv(self.notes))
  write("links.csv", links_to_csv(self.links))
  write("images.csv", images_to_csv(self.images))
  write("image_links.csv", image_links_to_csv(self.images))
  write("bibliography.csv", bibliography_to_csv(self.bibliography))
  write("citations.csv", citations_to_csv(self.citations))
end

return {
  SlipBox = SlipBox,
}
end
end

do
local _ENV = _ENV
package.preload[ "src.utils" ] = function( ... ) local arg = _G.arg;
local function hashtag_prefix(s)
  return s:match '^#[-_a-zA-Z0-9]+'
end

local function get_link(src, link)
  assert(link.tag == "Link")
  assert(type(src) == "number")
  if not link.target:match('^#%d+$') then return end
  return {
    src = src,
    dest = tonumber(link.target:sub(2)),
    description = link.title,
  }
end

local function append_text(filename, text)
  local file = io.open(filename, 'a')
  if not file then return false end
  file:write(text)
  file:close()
  return true
end

local function write_text(filename, text)
  local file = io.open(filename, 'w')
  if not file then return false end
  file:write(text)
  file:close()
  return true
end

local function strip(text)
  -- Strip leading and trailing whitespace.
  return text:match('^%s*(.-)%s*$')
end

local function parse_filename(text)
  local pattern = '^%[slipbox%-metadata%]\nfilename=(.-)$'
  local filename = text:match(pattern)
  if filename then
    return strip(filename)
  end
end

local function is_reference_id(text)
  -- Check if text (string) is a reference identifier.
  return text:match('^ref%-.+$') and true or false
end

return {
  is_reference_id = is_reference_id,
  hashtag_prefix = hashtag_prefix,
  get_link = get_link,
  parse_filename = parse_filename,
  write_text = write_text,
  append_text = append_text,
}
end
end

local filters = require "src.filters"
local slipbox = require "src.slipbox"

local current_slipbox = slipbox.SlipBox:new()

return {
  filters.preprocess(),
  filters.init(current_slipbox),
  filters.collect(current_slipbox),
  filters.hashtag(),
  filters.modify(current_slipbox),
  filters.citations(current_slipbox),
  filters.serialize(current_slipbox),
  filters.check(current_slipbox),
  filters.cleanup(),
}
