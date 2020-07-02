import chisel3._
import chisel3.util._

class {top_name} extends Module {{
  val io = IO(new Bundle{{}})
  /** Define your code here
   *
  val io = IO(new Bundle{{
    val sel = Input(UInt(1.W))
    val in0 = Input(UInt(1.W))
    val in1 = Input(UInt(1.W))
    val out = Output(UInt(1.W))
  }})
  io.out := (io.sel & io.in1) | (~io.sel & io.in0)
  */
}}

object Main extends App {{
  Driver.execute(args, () => new {top_name})
}}
