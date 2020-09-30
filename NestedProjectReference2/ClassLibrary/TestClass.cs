public static class TestClass
{
    public static void PrintMessage()
    {
        System.Console.WriteLine("Hello from ClassLibrary!");
        TestClass2.PrintMessage();
    }
}
