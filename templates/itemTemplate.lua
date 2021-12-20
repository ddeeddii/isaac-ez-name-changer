local mod = RegisterMod(%MODNAME, 1)

local items = {
	{%ITEMID, %NEWITEMNAME, %NEWDESCRIPTION}
}

if EID then
	for i,item in ipairs(items) do
		local EIDdescription = EID:getDescriptionObj(5, 100, item[1]).Description
		EID:addCollectible(item[1], EIDdescription, item[2], "en_us")
	end
end

if Encyclopedia then
	for i,item in ipairs(items) do
		Encyclopedia.UpdateItem(item[1], {
			Class = "vanilla",
			Name = item[2],
			Description = item[3],
		})
	end
end

local queueLastFrame
local queueNow
function mod.onUpdate(_, player)
	queueNow = player.QueuedItem.Item
	if (queueNow ~= nil) then	
		for i,item in ipairs(items) do
			if (queueNow.ID == item[1] and queueNow:IsCollectible() and queueLastFrame == nil) then
				Game():GetHUD():ShowItemText(item[2], item[3])
			end
		end
	end
	queueLastFrame = queueNow
end
mod:AddCallback(ModCallbacks.MC_POST_PLAYER_UPDATE, mod.onUpdate)

-- Generated with isaac-ez-name-changer