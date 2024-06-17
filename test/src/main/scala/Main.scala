@main def hello(): Unit =
  println("Hello world!")
  println(msg)

def msg = "I was compiled by Scala 3. :)"

import scala.concurrent.ExecutionContext.Implicits.global // Import for futures

val futureList: Future[List[Int]] = Future { List(1, 2, 3, 4) }

val futureInt: Future[Int] = futureList.map { list =>
    // Example: summing the elements
    list.sum
}
