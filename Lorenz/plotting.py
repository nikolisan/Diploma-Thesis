def setup_animation():
    init_figure()
    for line in lines:
        self.line = self.mplCanvas.canvas.ax.plot([], [], [])
    self.stopped = False