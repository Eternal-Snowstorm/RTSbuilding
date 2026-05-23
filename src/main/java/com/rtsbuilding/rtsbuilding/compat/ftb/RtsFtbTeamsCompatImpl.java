package com.rtsbuilding.rtsbuilding.compat.ftb;

import java.lang.reflect.Method;
import java.util.UUID;

import net.minecraft.server.level.ServerPlayer;

final class RtsFtbTeamsCompatImpl {
    private final Method teamsApiMethod;
    private final Method getTeamManagerMethod;
    private final Method getTeamForPlayerMethod;

    RtsFtbTeamsCompatImpl() throws ReflectiveOperationException {
        Class<?> ftbTeamsApiClass = Class.forName("dev.ftb.mods.ftbteams.api.FTBTeamsAPI");
        this.teamsApiMethod = ftbTeamsApiClass.getMethod("api");
        this.getTeamManagerMethod = this.teamsApiMethod.getReturnType().getMethod("getManager");
        this.getTeamForPlayerMethod = resolveTeamLookupMethod(this.getTeamManagerMethod.getReturnType());
    }

    String teamKey(ServerPlayer player) {
        if (player == null) {
            return "";
        }
        try {
            Object team = resolveTeam(player.getUUID());
            if (team == null) {
                return "";
            }
            String stableId = resolveStableTeamId(team);
            return stableId.isBlank() ? "" : "ftb:" + stableId;
        } catch (ReflectiveOperationException | RuntimeException ignored) {
            return "";
        }
    }

    private Object resolveTeam(UUID playerUuid) throws ReflectiveOperationException {
        Object api = this.teamsApiMethod.invoke(null);
        if (api == null) {
            return null;
        }
        Object manager = this.getTeamManagerMethod.invoke(api);
        if (manager == null) {
            return null;
        }
        return this.getTeamForPlayerMethod.invoke(manager, playerUuid);
    }

    private static String resolveStableTeamId(Object team) {
        for (String methodName : new String[] { "getId", "getTeamId", "getTeamID", "getUUID", "getUuid" }) {
            try {
                Method method = team.getClass().getMethod(methodName);
                if (method.getParameterCount() != 0) {
                    continue;
                }
                Object value = method.invoke(team);
                if (value instanceof UUID uuid) {
                    return uuid.toString();
                }
                if (value != null && !value.toString().isBlank()) {
                    return value.toString();
                }
            } catch (ReflectiveOperationException ignored) {
                // Try the next known id method name.
            }
        }
        return team.toString();
    }

    private static Method resolveTeamLookupMethod(Class<?> managerClass) throws NoSuchMethodException {
        for (String name : new String[] { "getTeamForPlayerID", "getTeamForPlayer" }) {
            try {
                return managerClass.getMethod(name, UUID.class);
            } catch (NoSuchMethodException ignored) {
                // Try next candidate.
            }
        }
        throw new NoSuchMethodException("Missing team lookup method on " + managerClass.getName());
    }
}
