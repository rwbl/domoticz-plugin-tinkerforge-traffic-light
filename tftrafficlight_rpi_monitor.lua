-- Tinkerforge RGBLEDV2 Bricklet Plugin - Test Script 
-- dzVents Automation Script: tftrafficlight_rpi_monitor
-- Use a RGBLED to indicate the CPU temperature depending level and set to R or Y or G.
-- 20200216 by rwbL

-- Idx devices.
IDXRPICPUTEMP = 2
IDXSTATESELECTOR  = 97

-- Define the state selector switch levels according the switch selector settings
LEVELRED = 10
LEVELYELLOW = 20
LEVELGREEN = 30

-- Define the cpu temp thresholds in C
THRED = 43
THGREEN = 42

return {
	on = {
		timer = {
			'every minute',
	   },
    },
	execute = function(domoticz, timer)
		domoticz.log('Timer event triggered by ' .. timer.trigger, domoticz.LOG_INFO)
    	-- Get the cputemp and log
    	local cputemp = tonumber(domoticz.devices(IDXRPICPUTEMP).sValue)
		domoticz.log(string.format('CPU Temperature: %.f', cputemp), domoticz.LOG_INFO)

        -- Device CPU Temperature set RGBLED color
        local newlevel = 0
        if (cputemp >= THRED) then newlevel = LEVELRED end
        if (cputemp >= THGREEN and cputemp < THRED) then newlevel = LEVELYELLOW end
        if (cputemp < THGREEN) then newlevel = LEVELGREEN end

        local oldlevel = domoticz.devices(IDXSTATESELECTOR).level
		domoticz.log(string.format('Level Old / New: %d/%d', oldlevel,newlevel), domoticz.LOG_INFO)
        if (newlevel ~= oldlevel) then domoticz.devices(IDXSTATESELECTOR).setLevel(newlevel) end
        -- Clear the device log
        domoticz.openURL('http://localhost:8080/json.htm?type=command&param=clearlightlog&idx=' .. IDXSTATESELECTOR)

    end
}
