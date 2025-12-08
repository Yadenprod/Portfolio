using System;
using System.Threading;
using OpenCvSharp;
using WindowsInput;
using WindowsInput.Native;

class Program
{
    // Настройки
    static readonly Scalar targetColor = new Scalar(250, 195, 248); // BGR!
    static readonly int tolerance = 50;
    static readonly int regionSize = 5; // область вокруг центра
    static readonly int delayMin = 80; // ms
    static readonly int delayMax = 140; // ms
    static readonly string cameraName = "OBS Virtual Camera";

    static void Main()
    {
        var sim = new InputSimulator();
        var capture = new VideoCapture(0); // 0 — обычно OBS Virtual Camera
        if (!capture.IsOpened())
        {
            Console.WriteLine("Не удалось открыть OBS Virtual Camera!");
            return;
        }
        Console.WriteLine("Triggerbot запущен. Для выхода закройте окно.");
        var frame = new Mat();
        var rand = new Random();
        while (true)
        {
            capture.Read(frame);
            if (frame.Empty()) continue;
            int w = frame.Width;
            int h = frame.Height;
            int cx = w / 2;
            int cy = h / 2;
            bool found = false;
            for (int dx = -regionSize / 2; dx <= regionSize / 2 && !found; dx++)
            {
                for (int dy = -regionSize / 2; dy <= regionSize / 2 && !found; dy++)
                {
                    var color = frame.At<Vec3b>(cy + dy, cx + dx);
                    if (ColorMatch(color, targetColor, tolerance))
                    {
                        sim.Keyboard.KeyDown(VirtualKeyCode.SPACE);
                        found = true;
                    }
                }
            }
            if (!found)
                sim.Keyboard.KeyUp(VirtualKeyCode.SPACE);
            Thread.Sleep(rand.Next(delayMin, delayMax));
        }
    }

    static bool ColorMatch(Vec3b color, Scalar target, int tol)
    {
        return Math.Abs(color.Item0 - target.Val0) <= tol &&
               Math.Abs(color.Item1 - target.Val1) <= tol &&
               Math.Abs(color.Item2 - target.Val2) <= tol;
    }
}
