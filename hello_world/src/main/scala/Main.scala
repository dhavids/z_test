
val forkJoinPool: ExecutorService = new ForkJoinPool(4)
implicit val forkJoinExecutionContext: ExecutionContext = 
  ExecutionContext.fromExecutorService(forkJoinPool)

val singleThread: Executor = Executors.newSingleThreadExecutor()
implicit val singleThreadExecutionContext: ExecutionContext = 
  ExecutionContext.fromExecutor(singleThread)

implicit val globalExecutionContext: ExecutionContext = ExecutionContext.global

def generateMagicNumber(): Int = {
  Thread.sleep(3000L)
  23
}
val generatedMagicNumberF: Future[Int] = Future {
  generateMagicNumber()
}