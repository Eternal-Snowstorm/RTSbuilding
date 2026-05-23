package com.rtsbuilding.rtsbuilding.client;

import com.rtsbuilding.rtsbuilding.RtsbuildingMod;

import com.mojang.blaze3d.systems.RenderSystem;

import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.RenderStateShard;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.LevelRenderer;
import net.minecraft.core.BlockPos;
import net.minecraft.core.SectionPos;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.projectile.ProjectileUtil;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RenderLevelStageEvent;

import com.mojang.blaze3d.vertex.BufferBuilder;
import com.mojang.blaze3d.vertex.ByteBufferBuilder;
import com.mojang.blaze3d.vertex.DefaultVertexFormat;
import com.mojang.blaze3d.vertex.MeshData;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.mojang.blaze3d.vertex.VertexFormat;

@EventBusSubscriber(modid = RtsbuildingMod.MODID, value = Dist.CLIENT, bus = EventBusSubscriber.Bus.GAME)
public final class RtsBoundaryRenderer {
    private static final int GL_LEQUAL = 515;

    private static final RenderType CHUNK_XRAY_LINES = RenderType.create(
            "rtsbuilding_chunk_xray_lines",
            DefaultVertexFormat.POSITION_COLOR_NORMAL,
            VertexFormat.Mode.LINES,
            8192,
            RenderType.CompositeState.builder()
                    .setShaderState(RenderStateShard.RENDERTYPE_LINES_SHADER)
                    .setLineState(RenderStateShard.DEFAULT_LINE)
                    .setTransparencyState(RenderStateShard.TRANSLUCENT_TRANSPARENCY)
                    .setDepthTestState(RenderStateShard.NO_DEPTH_TEST)
                    .setOutputState(RenderStateShard.MAIN_TARGET)
                    .setWriteMaskState(RenderStateShard.COLOR_WRITE)
                    .setCullState(RenderStateShard.NO_CULL)
                    .createCompositeState(false));

    private RtsBoundaryRenderer() {
    }

    @SubscribeEvent
    public static void onRenderLevel(RenderLevelStageEvent event) {
        if (event.getStage() != RenderLevelStageEvent.Stage.AFTER_TRANSLUCENT_BLOCKS) {
            return;
        }

        ClientRtsController controller = ClientRtsController.get();
        if (!controller.hasBounds()) {
            return;
        }

        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.level == null) {
            return;
        }

        Vec3 camPos = event.getCamera().getPosition();
        PoseStack poseStack = event.getPoseStack();
        poseStack.pushPose();
        poseStack.translate(-camPos.x, -camPos.y, -camPos.z);

        if (controller.isChunkCurtainVisible()) {
            RenderType chunkLines = CHUNK_XRAY_LINES;
            try (ByteBufferBuilder chunkLineBacking = new ByteBufferBuilder(chunkLines.bufferSize())) {
                BufferBuilder chunkLineBuffer = new BufferBuilder(chunkLineBacking, chunkLines.mode, chunkLines.format);
                renderChunkGuides(minecraft, controller, poseStack, chunkLineBuffer);
                drawBuiltBufferNoDepth(chunkLines, chunkLineBuffer);
            }
        }

        RenderType lines = RenderType.lines();
        RenderType filledBox = RenderType.debugFilledBox();
        try (ByteBufferBuilder lineBacking = new ByteBufferBuilder(lines.bufferSize());
                ByteBufferBuilder fillBacking = new ByteBufferBuilder(filledBox.bufferSize())) {
            BufferBuilder lineBuffer = new BufferBuilder(lineBacking, lines.mode, lines.format);
            BufferBuilder fillBuffer = new BufferBuilder(fillBacking, filledBox.mode, filledBox.format);

            double ax = controller.getAnchorX();
            double ay = controller.getAnchorY();
            double az = controller.getAnchorZ();
            double r = controller.getMaxRadius();

            double minX = ax - r;
            double maxX = ax + r;
            double minZ = az - r;
            double maxZ = az + r;

            // Drag limit boundary (3 chunks radius => 48 blocks)
            LevelRenderer.renderLineBox(poseStack, lineBuffer, minX, ay - 0.25D, minZ, maxX, ay + 0.25D, maxZ,
                    1.0F, 0.25F, 0.25F, 1.0F);

            renderLinkedStorages(minecraft, controller, poseStack, lineBuffer);
            renderHoveredInteractionTarget(minecraft, controller, poseStack, lineBuffer);
            renderShapeGhostPreview(minecraft, poseStack, lineBuffer, fillBuffer);

            drawBuiltBuffer(lines, lineBuffer);
            drawBuiltBuffer(filledBox, fillBuffer);
        }
        poseStack.popPose();
    }

    private static void drawBuiltBuffer(RenderType renderType, BufferBuilder buffer) {
        MeshData meshData = buffer.build();
        if (meshData != null) {
            renderType.draw(meshData);
        }
    }

    private static void drawBuiltBufferNoDepth(RenderType renderType, BufferBuilder buffer) {
        MeshData meshData = buffer.build();
        if (meshData != null) {
            RenderSystem.disableDepthTest();
            RenderSystem.depthMask(false);
            renderType.draw(meshData);
            RenderSystem.depthMask(true);
            RenderSystem.enableDepthTest();
            RenderSystem.depthFunc(GL_LEQUAL);
        }
    }

    private static void renderChunkGuides(
            Minecraft minecraft,
            ClientRtsController controller,
            PoseStack poseStack,
            VertexConsumer lineBuffer) {
        if (minecraft.level == null) {
            return;
        }
        int anchorChunkX = SectionPos.blockToSectionCoord(Mth.floor(controller.getAnchorX()));
        int anchorChunkZ = SectionPos.blockToSectionCoord(Mth.floor(controller.getAnchorZ()));
        int chunkRange = Math.max(1, Mth.ceil(controller.getMaxRadius() / 16.0D));
        int minChunkX = anchorChunkX - chunkRange;
        int maxChunkX = anchorChunkX + chunkRange;
        int minChunkZ = anchorChunkZ - chunkRange;
        int maxChunkZ = anchorChunkZ + chunkRange;
        double zMin = (anchorChunkZ - chunkRange) * 16.0D;
        double zMax = (anchorChunkZ + chunkRange + 1) * 16.0D;
        double xMin = (anchorChunkX - chunkRange) * 16.0D;
        double xMax = (anchorChunkX + chunkRange + 1) * 16.0D;
        double y = Math.floor(controller.getAnchorY()) + 0.06D;

        for (int cx = minChunkX; cx <= maxChunkX + 1; cx++) {
            double x = cx * 16.0D;
            renderFlatChunkLineX(poseStack, lineBuffer, x, y, zMin, zMax);
        }
        for (int cz = minChunkZ; cz <= maxChunkZ + 1; cz++) {
            double z = cz * 16.0D;
            renderFlatChunkLineZ(poseStack, lineBuffer, z, y, xMin, xMax);
        }
    }

    private static void renderFlatChunkLineX(
            PoseStack poseStack,
            VertexConsumer lineBuffer,
            double x,
            double y,
            double zMin,
            double zMax) {
        double halfWidth = 0.018D;
        double halfHeight = 0.035D;
        LevelRenderer.renderLineBox(
                poseStack,
                lineBuffer,
                x - halfWidth,
                y - halfHeight,
                zMin,
                x + halfWidth,
                y + halfHeight,
                zMax,
                0.18F,
                0.96F,
                1.0F,
                0.95F);
    }

    private static void renderFlatChunkLineZ(
            PoseStack poseStack,
            VertexConsumer lineBuffer,
            double z,
            double y,
            double xMin,
            double xMax) {
        double halfWidth = 0.018D;
        double halfHeight = 0.035D;
        LevelRenderer.renderLineBox(
                poseStack,
                lineBuffer,
                xMin,
                y - halfHeight,
                z - halfWidth,
                xMax,
                y + halfHeight,
                z + halfWidth,
                0.18F,
                0.96F,
                1.0F,
                0.95F);
    }

    private static void renderLinkedStorages(Minecraft minecraft, ClientRtsController controller, PoseStack poseStack,
            VertexConsumer lineBuffer) {
        if (minecraft.level == null || controller.getLinkedStoragePositions().isEmpty()) {
            return;
        }

        for (BlockPos pos : controller.getLinkedStoragePositions()) {
            if (!minecraft.level.hasChunkAt(pos)) {
                continue;
            }
            BlockState state = minecraft.level.getBlockState(pos);
            if (state.isAir()) {
                continue;
            }

            LevelRenderer.renderLineBox(
                    poseStack,
                    lineBuffer,
                    pos.getX() - 0.002D,
                    pos.getY() - 0.002D,
                    pos.getZ() - 0.002D,
                    pos.getX() + 1.002D,
                    pos.getY() + 1.002D,
                    pos.getZ() + 1.002D,
                    0.24F, 0.55F, 1.00F, 1.0F);
        }
    }

    private static void renderHoveredInteractionTarget(Minecraft minecraft, ClientRtsController controller,
            PoseStack poseStack, VertexConsumer lineBuffer) {
        if (controller.isRotateCaptured() || minecraft.level == null || minecraft.getCameraEntity() == null) {
            return;
        }

        Vec3 camPos = minecraft.gameRenderer.getMainCamera().getPosition();
        Vec3 viewDir = computeCursorRayDirection(minecraft);
        Vec3 to = camPos.add(viewDir.scale(128.0D));
        BlockHitResult blockHit = raycastBlockFromCursor(minecraft, camPos, to, false);
        EntityHitResult entityHit = raycastEntityFromCursor(minecraft, camPos, to, viewDir, 128.0D);
        double blockDist = blockHit != null ? camPos.distanceToSqr(blockHit.getLocation()) : Double.MAX_VALUE;
        double entityDist = entityHit != null ? camPos.distanceToSqr(entityHit.getLocation()) : Double.MAX_VALUE;

        if (entityHit != null && entityDist <= blockDist) {
            Entity entity = entityHit.getEntity();
            AABB bb = entity.getBoundingBox().inflate(0.03D);
            LevelRenderer.renderLineBox(
                    poseStack,
                    lineBuffer,
                    bb.minX,
                    bb.minY,
                    bb.minZ,
                    bb.maxX,
                    bb.maxY,
                    bb.maxZ,
                    0.35F,
                    1.0F,
                    0.55F,
                    1.0F);
            return;
        }
        if (blockHit == null || blockHit.getType() != HitResult.Type.BLOCK) {
            return;
        }

        BlockPos pos = blockHit.getBlockPos();
        BlockState state = minecraft.level.getBlockState(pos);
        if (state.isAir()) {
            LevelRenderer.renderLineBox(
                    poseStack,
                    lineBuffer,
                    pos.getX(),
                    pos.getY(),
                    pos.getZ(),
                    pos.getX() + 1.0D,
                    pos.getY() + 1.0D,
                    pos.getZ() + 1.0D,
                    1.0F, 0.95F, 0.2F, 1.0F);
            return;
        }

        var shape = state.getShape(minecraft.level, pos);
        if (shape.isEmpty()) {
            LevelRenderer.renderLineBox(
                    poseStack,
                    lineBuffer,
                    pos.getX(),
                    pos.getY(),
                    pos.getZ(),
                    pos.getX() + 1.0D,
                    pos.getY() + 1.0D,
                    pos.getZ() + 1.0D,
                    1.0F, 0.95F, 0.2F, 1.0F);
            return;
        }

        for (AABB box : shape.toAabbs()) {
            LevelRenderer.renderLineBox(
                    poseStack,
                    lineBuffer,
                    pos.getX() + box.minX,
                    pos.getY() + box.minY,
                    pos.getZ() + box.minZ,
                    pos.getX() + box.maxX,
                    pos.getY() + box.maxY,
                    pos.getZ() + box.maxZ,
                    1.0F, 0.95F, 0.2F, 1.0F);
        }
    }

    private static void renderShapeGhostPreview(Minecraft minecraft, PoseStack poseStack, VertexConsumer lineBuffer,
            VertexConsumer fillBuffer) {
        if (!(minecraft.screen instanceof BuilderScreen builderScreen)) {
            return;
        }
        BuilderScreen.ShapeGhostPreview preview = builderScreen.getShapeGhostPreview();
        if (preview.blocks().isEmpty()) {
            return;
        }

        float lineR = preview.readyConfirm() ? 0.45F : 0.30F;
        float lineG = preview.readyConfirm() ? 0.95F : 0.75F;
        float lineB = preview.readyConfirm() ? 0.45F : 1.00F;
        float fillR = preview.readyConfirm() ? 0.24F : 0.16F;
        float fillG = preview.readyConfirm() ? 0.72F : 0.55F;
        float fillB = preview.readyConfirm() ? 0.24F : 0.90F;
        float fillA = preview.readyConfirm() ? 0.22F : 0.16F;

        for (BlockPos pos : preview.blocks()) {
            double minX = pos.getX() + 0.03D;
            double minY = pos.getY() + 0.03D;
            double minZ = pos.getZ() + 0.03D;
            double maxX = pos.getX() + 0.97D;
            double maxY = pos.getY() + 0.97D;
            double maxZ = pos.getZ() + 0.97D;
            LevelRenderer.addChainedFilledBoxVertices(
                    poseStack,
                    fillBuffer,
                    minX,
                    minY,
                    minZ,
                    maxX,
                    maxY,
                    maxZ,
                    fillR,
                    fillG,
                    fillB,
                    fillA);
        }

        for (BlockPos pos : preview.blocks()) {
            double minX = pos.getX() + 0.03D;
            double minY = pos.getY() + 0.03D;
            double minZ = pos.getZ() + 0.03D;
            double maxX = pos.getX() + 0.97D;
            double maxY = pos.getY() + 0.97D;
            double maxZ = pos.getZ() + 0.97D;
            LevelRenderer.renderLineBox(
                    poseStack,
                    lineBuffer,
                    minX,
                    minY,
                    minZ,
                    maxX,
                    maxY,
                    maxZ,
                    lineR,
                    lineG,
                    lineB,
                    0.95F);
        }
    }

    private static BlockHitResult raycastBlockFromCursor(Minecraft minecraft, Vec3 camPos, Vec3 to,
            boolean includeFluidSource) {
        ClipContext.Fluid fluidMode = includeFluidSource ? ClipContext.Fluid.SOURCE_ONLY : ClipContext.Fluid.NONE;
        HitResult hit = minecraft.level.clip(new ClipContext(camPos, to, ClipContext.Block.OUTLINE, fluidMode,
                minecraft.getCameraEntity()));
        if (hit instanceof BlockHitResult bhr && hit.getType() == HitResult.Type.BLOCK) {
            return bhr;
        }
        return null;
    }

    private static EntityHitResult raycastEntityFromCursor(Minecraft minecraft, Vec3 camPos, Vec3 to, Vec3 viewDir,
            double reach) {
        Entity cameraEntity = minecraft.getCameraEntity();
        if (cameraEntity == null) {
            return null;
        }
        AABB search = cameraEntity.getBoundingBox().expandTowards(viewDir.scale(reach)).inflate(1.0D);
        return ProjectileUtil.getEntityHitResult(
                cameraEntity,
                camPos,
                to,
                search,
                entity -> entity != null
                        && entity.isAlive()
                        && entity.isPickable()
                        && entity != cameraEntity
                        && entity != minecraft.player,
                reach * reach);
    }

    private static Vec3 computeCursorRayDirection(Minecraft minecraft) {
        double mouseX = minecraft.mouseHandler.xpos();
        double mouseY = minecraft.mouseHandler.ypos();
        double width = Math.max(1.0D, minecraft.getWindow().getScreenWidth());
        double height = Math.max(1.0D, minecraft.getWindow().getScreenHeight());

        double nx = (mouseX / width) * 2.0D - 1.0D;
        double ny = 1.0D - (mouseY / height) * 2.0D;

        float yawDeg = minecraft.gameRenderer.getMainCamera().getYRot();
        float pitchDeg = minecraft.gameRenderer.getMainCamera().getXRot();
        double yaw = Math.toRadians(yawDeg);
        double pitch = Math.toRadians(pitchDeg);

        Vec3 forward = new Vec3(
                -Math.sin(yaw) * Math.cos(pitch),
                -Math.sin(pitch),
                Math.cos(yaw) * Math.cos(pitch)).normalize();

        Vec3 right = new Vec3(Math.cos(yaw), 0.0D, Math.sin(yaw)).normalize();
        Vec3 up = forward.cross(right).normalize();

        double fovY = Math.toRadians(minecraft.options.fov().get());
        double tanY = Math.tan(fovY * 0.5D);
        double tanX = tanY * (width / height);

        // Current yaw basis yields a left-vector here; invert X NDC to keep screen-right -> ray-right.
        return forward.add(right.scale(-nx * tanX)).add(up.scale(ny * tanY)).normalize();
    }
}
