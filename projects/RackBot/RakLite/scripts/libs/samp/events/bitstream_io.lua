-- This file is part of the SAMP.Lua project.
-- Licensed under the MIT License.
-- Copyright (c) 2016, FYP @ BlastHack Team <blast.hk>
-- https://github.com/THE-FYP/SAMP.Lua

local mod = {}
local vector3d = require 'vector3d'
local ffi = require 'ffi'

local function bitstream_read_fixed_string(bs, size)
	local buf = ffi.new('uint8_t[?]', size + 1)
	bs:readBuffer(tonumber(ffi.cast('intptr_t', buf)), size)
	buf[size] = 0
	-- Length is not specified to throw off trailing zeros.
	return ffi.string(buf)
end

local function bitstream_write_fixed_string(bs, str, size)
	local buf = ffi.new('uint8_t[?]', size, string.sub(str, 1, size))
	bs:writeBuffer(tonumber(ffi.cast('intptr_t', buf)), size)
end

mod.bool = {
	read = function(bs) return bs:readBool() end,
	write = function(bs, value) return bs:writeBool(value) end
}

mod.uint8 = {
	read = function(bs) return bs:readUInt8() end,
	write = function(bs, value) return bs:writeUInt8(value) end
}

mod.uint16 = {
	read = function(bs) return bs:readUInt16() end,
	write = function(bs, value) return bs:writeUInt16(value) end
}

mod.uint32 = {
	read = function(bs) return bs:readUInt32() end,
	write = function(bs, value) return bs:writeUInt32(value) end
}

mod.int8 = {
	read = function(bs) return bs:readInt8() end,
	write = function(bs, value) return bs:writeInt8(value) end
}

mod.int16 = {
	read = function(bs) return bs:readInt16() end,
	write = function(bs, value) return bs:writeInt16(value) end
}

mod.int32 = {
	read = function(bs) return bs:readInt32() end,
	write = function(bs, value) return bs:writeInt32(value) end
}

mod.float = {
	read = function(bs) return bs:readFloat() end,
	write = function(bs, value) return bs:writeFloat(value) end
}

mod.string8 = {
	read = function(bs)
		local len =  bs:readUInt8()
		if len <= 0 then return '' end
		return bs:readString(len)
	end,
	write = function(bs, value)
		bs:writeUInt8(#value)
		bs:writeString(value)
	end
}

mod.string16 = {
	read = function(bs)
		local len = bs:readUInt16()
		if len <= 0 then return '' end
		return bs:readString(len)
	end,
	write = function(bs, value)
		bs:writeUInt16(#value)
		bs:writeString(value)
	end
}

mod.string32 = {
	read = function(bs)
		local len = bs:readUInt32()
		if len <= 0 then return '' end
		return bs:readString(len)
	end,
	write = function(bs, value)
		bs:writeUInt32(#value)
		bs:writeString(value)
	end
}

mod.bool8 = {
	read = function(bs)
		return bs:readUInt8() ~= 0
	end,
	write = function(bs, value)
		bs:writeUInt8(value == true and 1 or 0)
	end
}

mod.bool32 = {
	read = function(bs)
		return bs:readUInt32() ~= 0
	end,
	write = function(bs, value)
		bs:writeUInt32(value == true and 1 or 0)
	end
}

mod.int1 = {
	read = function(bs)
		if bs:readBool() == true then return 1 else return 0 end
	end,
	write = function(bs, value)
		bs:writeBool(value ~= 0 and true or false)
	end
}

mod.fixedString32 = {
	read = function(bs)
		return bitstream_read_fixed_string(bs, 32)
	end,
	write = function(bs, value)
		bitstream_write_fixed_string(bs, value, 32)
	end
}

mod.string256 = mod.fixedString32

mod.encodedString2048 = {
	read = function(bs) return bs:readEncoded(2048) end,
	write = function(bs, value) bs:writeEncoded(value) end
}

mod.encodedString4096 = {
	read = function(bs) return bs:readEncoded(4096) end,
	write = function(bs, value) bs:writeEncoded(value) end
}

mod.compressedFloat = {
	read = function(bs)
		return bs:readUInt16() / 32767.5 - 1
	end,
	write = function(bs, value)
		if value < -1 then
			value = -1
		elseif value > 1 then
			value = 1
		end
		bs:writeUInt16((value + 1) * 32767.5)
	end
}

mod.compressedVector = {
	read = function(bs)
		local magnitude = bs:readFloat()
		if magnitude ~= 0 then
			return vector3d(mod.compressedFloat.read(bs) * magnitude, mod.compressedFloat.read(bs) * magnitude, mod.compressedFloat.read(bs) * magnitude)
		else
			return vector3d(0, 0, 0)
		end
	end,
	write = function(bs, data)
		local x, y, z = data.x, data.y, data.z
		local magnitude = math.sqrt(x * x + y * y + z * z)
		bs:writeFloat(magnitude)
		if magnitude > 0 then
			mod.compressedFloat.write(bs, x / magnitude)
			mod.compressedFloat.write(bs, y / magnitude)
			mod.compressedFloat.write(bs, z / magnitude)
		end
	end
}

mod.normQuat = {
	read = function(bs)
		local cwNeg, cxNeg, cyNeg, czNeg = bs:readBool(), bs:readBool(), bs:readBool(), bs:readBool()
		local cx, cy, cz = bs:readUInt16(), bs:readUInt16(), bs:readUInt16()
		local x = cx / 65535
		local y = cy / 65535
		local z = cz / 65535
		if cxNeg then x = -x end
		if cyNeg then y = -y end
		if czNeg then z = -z end
		local diff = 1 - x * x - y * y - z * z
		if diff < 0 then diff = 0 end
		local w = math.sqrt(diff)
		if cwNeg then w = -w end
		return {w, x, y, z}
	end,
	write = function(bs, value)
		local w, x, y, z = value[1], value[2], value[3], value[4]
		bs:writeBool(w < 0)
		bs:writeBool(x < 0)
		bs:writeBool(y < 0)
		bs:writeBool(z < 0)
		bs:writeUInt16(math.abs(x) * 65535)
		bs:writeUInt16(math.abs(y) * 65535)
		bs:writeUInt16(math.abs(z) * 65535)
		-- w is calculated on the target
	end
}

mod.vector3d = {
	read = function(bs)
		local x, y, z =
			bs:readFloat(),
			bs:readFloat(),
			bs:readFloat()
		return vector3d(x, y, z)
	end,
	write = function(bs, value)
		bs:writeFloat(value.x)
		bs:writeFloat(value.y)
		bs:writeFloat(value.z)
	end
}

mod.vector2d = {
	read = function(bs)
		local x = bs:readFloat()
		local y = bs:readFloat()
		return {x = x, y = y}
	end,
	write = function(bs, value)
		bs:writeFloat(value.x)
		bs:writeFloat(value.y)
	end
}

local function bitstream_io_interface(field)
	return setmetatable({}, {
		__index = function(t, index)
			return mod[index][field]
		end
	})
end

mod.bs_read = bitstream_io_interface('read')
mod.bs_write = bitstream_io_interface('write')

return mod
