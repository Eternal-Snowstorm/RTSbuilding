package com.rtsbuilding.rtsbuilding.client;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import com.rtsbuilding.rtsbuilding.Config;
import com.rtsbuilding.rtsbuilding.progression.RtsProgressionNode;
import com.rtsbuilding.rtsbuilding.progression.RtsProgressionNodes;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.EditBox;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;

public final class RtsModConfigScreen extends Screen {
    private final Screen parent;
    private final List<RtsProgressionNode> nodes = new ArrayList<>(RtsProgressionNodes.all());
    private final List<EditBox> costBoxes = new ArrayList<>();
    private final Map<ResourceLocation, String> draftCosts = new LinkedHashMap<>();
    private boolean survivalEnabled = Config.ENABLE_SURVIVAL_PROGRESSION.getAsBoolean();
    private boolean shareWithTeams = Config.SHARE_SURVIVAL_PROGRESSION_WITH_TEAMS.getAsBoolean();
    private int scroll;

    public RtsModConfigScreen(Screen parent) {
        super(Component.literal("RTSBuilding Config"));
        this.parent = parent;
    }

    @Override
    protected void init() {
        if (this.draftCosts.isEmpty()) {
            for (RtsProgressionNode node : this.nodes) {
                this.draftCosts.put(node.id(), RtsProgressionNodes.costTextFor(node));
            }
        }
        rebuildConfigWidgets();
    }

    private void rebuildConfigWidgets() {
        captureVisibleDrafts();
        clearWidgets();
        this.costBoxes.clear();

        int panelW = Math.min(420, this.width - 24);
        int x = (this.width - panelW) / 2;
        int y = 18;

        addRenderableWidget(Button.builder(Component.literal(this.survivalEnabled ? "Survival Balance: ON" : "Survival Balance: OFF"), btn -> {
            this.survivalEnabled = !this.survivalEnabled;
            rebuildConfigWidgets();
        }).bounds(x + 12, y + 30, 186, 20).build());
        addRenderableWidget(Button.builder(Component.literal(this.shareWithTeams ? "Shared Teams: ON" : "Shared Teams: OFF"), btn -> {
            this.shareWithTeams = !this.shareWithTeams;
            rebuildConfigWidgets();
        }).bounds(x + 208, y + 30, 186, 20).build());

        int listY = y + 72;
        int rows = visibleRows();
        this.scroll = Mth.clamp(this.scroll, 0, maxScroll());
        for (int row = 0; row < rows; row++) {
            int nodeIndex = row + this.scroll;
            if (nodeIndex >= this.nodes.size()) {
                break;
            }
            RtsProgressionNode node = this.nodes.get(nodeIndex);
            EditBox box = new EditBox(this.font, x + 154, listY + row * 24 + 3, panelW - 226, 16, Component.literal(node.id().getPath()));
            box.setMaxLength(512);
            box.setValue(this.draftCosts.getOrDefault(node.id(), RtsProgressionNodes.costTextFor(node)));
            addRenderableWidget(box);
            this.costBoxes.add(box);

            final int capturedIndex = nodeIndex;
            addRenderableWidget(Button.builder(Component.literal("Reset"), btn -> {
                RtsProgressionNode resetNode = this.nodes.get(capturedIndex);
                this.draftCosts.put(resetNode.id(), resetNode.costs().isEmpty() ? "" : RtsProgressionNodes.formatCostText(resetNode.costs()));
                rebuildConfigWidgets();
            }).bounds(x + panelW - 62, listY + row * 24 + 2, 50, 18).build());
        }

        addRenderableWidget(Button.builder(Component.literal("Save"), btn -> saveAndClose())
                .bounds(x + panelW - 118, this.height - 28, 54, 20)
                .build());
        addRenderableWidget(Button.builder(Component.literal("Back"), btn -> this.minecraft.setScreen(this.parent))
                .bounds(x + panelW - 58, this.height - 28, 46, 20)
                .build());
    }

    @Override
    public void render(GuiGraphics g, int mouseX, int mouseY, float partialTick) {
        int panelW = Math.min(420, this.width - 24);
        int x = (this.width - panelW) / 2;
        int y = 18;
        g.fill(x, y, x + panelW, this.height - 34, 0xEE101820);
        g.hLine(x, x + panelW, y, 0xFF6E8799);
        g.hLine(x, x + panelW, this.height - 34, 0xFF0D1218);
        g.drawString(this.font, "RTSBuilding Mod Config", x + 10, y + 9, 0xFFFFFF);
        g.drawString(this.font, "Server authority: multiplayer clients follow the server state.", x + 10, y + 56, 0xAFC2D4);
        g.drawString(this.font, "Skill material costs", x + 10, y + 72, 0xF4F7FF);

        int listY = y + 88;
        int rows = visibleRows();
        for (int row = 0; row < rows; row++) {
            int nodeIndex = row + this.scroll;
            if (nodeIndex >= this.nodes.size()) {
                break;
            }
            RtsProgressionNode node = this.nodes.get(nodeIndex);
            int rowY = listY + row * 24;
            g.fill(x + 8, rowY, x + panelW - 8, rowY + 22, row % 2 == 0 ? 0x5519222D : 0x55202A36);
            g.drawString(this.font, trim(node.id().getPath().replace('_', ' '), 130), x + 14, rowY + 7, 0xD9E6F2);
        }

        if (maxScroll() > 0) {
            g.drawString(this.font, (this.scroll + 1) + "/" + (maxScroll() + 1), x + panelW - 48, y + 72, 0xAFC2D4);
        }
        super.render(g, mouseX, mouseY, partialTick);
    }

    @Override
    public boolean mouseScrolled(double mouseX, double mouseY, double scrollX, double scrollY) {
        int next = this.scroll - (int) Math.signum(scrollY);
        next = Mth.clamp(next, 0, maxScroll());
        if (next != this.scroll) {
            this.scroll = next;
            rebuildConfigWidgets();
            return true;
        }
        return super.mouseScrolled(mouseX, mouseY, scrollX, scrollY);
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    private int visibleRows() {
        return Math.max(1, (this.height - 134) / 24);
    }

    private int maxScroll() {
        return Math.max(0, this.nodes.size() - visibleRows());
    }

    private void saveAndClose() {
        captureVisibleDrafts();
        Config.setSurvivalProgressionEnabled(this.survivalEnabled);
        Config.SHARE_SURVIVAL_PROGRESSION_WITH_TEAMS.set(this.shareWithTeams);
        Config.SPEC.save();
        for (RtsProgressionNode node : this.nodes) {
            Config.setProgressionCostOverride(node.id().getPath(), this.draftCosts.getOrDefault(node.id(), ""));
        }
        this.minecraft.setScreen(this.parent);
    }

    private void captureVisibleDrafts() {
        for (int i = 0; i < this.costBoxes.size(); i++) {
            int nodeIndex = this.scroll + i;
            if (nodeIndex < this.nodes.size()) {
                this.draftCosts.put(this.nodes.get(nodeIndex).id(), this.costBoxes.get(i).getValue());
            }
        }
    }

    private String trim(String text, int width) {
        return this.font.plainSubstrByWidth(text, width);
    }
}
