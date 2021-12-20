local mod = RegisterMod(%MODNAME, 1)

local trinkets = {
	{%ITEMID, %NEWITEMNAME, %NEWDESCRIPTION}
}

if EID then
	for t,trinket in ipairs(trinkets) do
		local EIDdescription = EID:getDescriptionObj(5, 350, trinket[1]).Description
		EID:addTrinket(trinket[1], EIDdescription, trinket[2], "en_us")
	end
end

if Encyclopedia then
	for t,trinket in ipairs(trinkets) do
		Encyclopedia.UpdateTrinket(trinket[1], {
			Name = trinket[2],
			Description = trinket[3],
			WikiDesc = trinket[4]
		})
	end
end

local queueLastFrame
local queueNow
function mod.onUpdate(_, player)
	queueNow = player.QueuedItem.Item
	if (queueNow ~= nil) then
		for t,trinket in ipairs(trinkets) do
			if (queueNow.ID == trinket[1] and queueNow:IsTrinket() and queueLastFrame == nil) then
				Game():GetHUD():ShowItemText(trinket[2], trinket[3])
			end
		end
	end
	queueLastFrame = queueNow
end
mod:AddCallback(ModCallbacks.MC_POST_PLAYER_UPDATE, mod.onUpdate)

-- Generated with isaac-ez-name-changer