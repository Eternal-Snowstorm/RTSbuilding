package com.rtsbuilding.rtsbuilding.network;

import com.rtsbuilding.rtsbuilding.RtsbuildingMod;

import net.minecraft.core.BlockPos;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

public record C2SRtsUltiminePayload(
        BlockPos pos,
        byte face,
        byte toolSlot,
        String toolItemId,
        short limit) implements CustomPacketPayload {
    public static final Type<C2SRtsUltiminePayload> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(RtsbuildingMod.MODID, "c2s_rts_ultimine"));

    public static final StreamCodec<RegistryFriendlyByteBuf, C2SRtsUltiminePayload> STREAM_CODEC = StreamCodec.of(
            (buf, payload) -> {
                buf.writeBlockPos(payload.pos());
                buf.writeByte(payload.face());
                buf.writeByte(payload.toolSlot());
                buf.writeUtf(payload.toolItemId() == null ? "" : payload.toolItemId(), 256);
                buf.writeShort(payload.limit());
            },
            (buf) -> new C2SRtsUltiminePayload(
                    buf.readBlockPos(),
                    buf.readByte(),
                    buf.readByte(),
                    buf.readUtf(256),
                    buf.readShort()));

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
