import android.app.ProgressDialog
import android.content.Context
import android.util.Log
import android.widget.Toast
import com.example.project.PacketViewModel
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.IOException
import java.io.InputStream
import java.io.OutputStream
import java.net.InetAddress
import java.net.ServerSocket
import java.net.Socket

// 기능 : 1:1 TCP/IP 소켓 통신을 위한 클래스, 일반적인 인자 통신과 스트리밍을 위한 인자 통신 함수가 있음

class NetworkManager {

    private val port = 7777
    private val maxBuf = 512
    private val ipAddress = "192.168.0.4"

    private lateinit var serverSocket: ServerSocket
    private lateinit var clientSocket: Socket
    private lateinit var outputStream: OutputStream
    private lateinit var inputStream: InputStream


    // 기능 : 서버 소켓을 생성하는 함수

    fun setTCPServerSocket() {
        try {
            serverSocket = ServerSocket(port)
        } catch (e: IOException) {
            Log.e("NetworkManager", "Failed to make serverSocket: ${e.message}")
            throw e
        }

    }

    // 기능 : 서버에 연결하는 함수. 클라이언트 소켓을 생성하고, 출력 및 입력 스트림을 설정
    fun connectToServer() {
        try {
            val serverAddress = InetAddress.getByName(ipAddress)
            clientSocket = Socket(serverAddress, port)
            outputStream = clientSocket.getOutputStream()
            inputStream = clientSocket.getInputStream()
        } catch (e: IOException) {
            Log.e("NetworkManager", "Failed to connect to the server: ${e.message}")
            throw e
        }
    }

    // 기능 : 데이터를 수신하는 함수. 입력 스트림에서 데이터를 읽어들이고 해당 데이터를 바이트 배열로 반환
    fun receiveData(): ByteArray {
        try {
            val buffer = ByteArray(maxBuf)
            val bytesRead = inputStream.read(buffer)
            return buffer.copyOf(bytesRead)
        } catch (e: IOException) {
            Log.e("NetworkManager", "Failed to receiveData: ${e.message}")
            throw e
        }
    }

    // 기능 : 데이터를 송신하는 함수. 출력 스트림을 사용하여 데이터를 서버로 전송
    fun sendData(data: ByteArray) {
        try {
            outputStream.write(data)
            outputStream.flush()
        } catch (e: IOException) {
            Log.e("NetworkManager", "Failed to receiveData: ${e.message}")
            throw e
        }
    }

    // 기능 : 서버로 패킷을 전송하는 함수 비동기적으로 실행되며, 통신이 끝날 때 까지 로딩하는 기능 존재
    fun sendPacketToServer(
        packetData: ByteArray,
        packetViewModel: PacketViewModel,
        context: Context
    ) {
        CoroutineScope(Dispatchers.IO).launch {
            var progressDialog: ProgressDialog? = null

            try {
                withContext(Dispatchers.Main) {
                    // 로딩 화면 출력
                    progressDialog = ProgressDialog(context)
                    progressDialog?.setMessage("로딩중...")
                    progressDialog?.setCancelable(false)
                    progressDialog?.show()
                }
                setTCPServerSocket()
                connectToServer()

                sendData(packetData)

                val responsePacket = receiveData()
                Log.d("Response", "Response: ${packetViewModel.parsingPacket(responsePacket)}")

                close()
                withContext(Dispatchers.Main) {
                    // 로딩 화면 닫기
                    progressDialog?.dismiss()
                }
            } catch (e: IOException) {
                Log.e("NetworkManager", "Failed to send packet to the server: ${e.message}")
                withContext(Dispatchers.Main) {
                    progressDialog?.dismiss()
                    Toast.makeText(context, "패킷 전송 실패", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }

    // 기능 : 서버로 패킷을 전송하고, 결과를 비동기적으로 반환하는 함수. 스트리밍을 위해 콜백을 사용하여 응답을 처리
    fun sendPacketToServer2(
        packetData: ByteArray,
        packetViewModel: PacketViewModel,
        requireContext: () -> Context,
        callback: (ByteArray?) -> Unit
    ) {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                setTCPServerSocket()
                connectToServer()

                sendData(packetData)

                val responsePacket = receiveData()
                Log.d("Response", "Response: ${packetViewModel.parsingPacket(responsePacket)}")

                close()

                callback(responsePacket)
            } catch (e: IOException) {
                Log.e("NetworkManager", "Failed to send packet to the server: ${e.message}")
                withContext(Dispatchers.Main) {
                    Toast.makeText(requireContext(), "패킷 전송 실패", Toast.LENGTH_SHORT).show()
                }

                callback(null)
            }
        }
    }
            // 기능 :  소켓 연결을 닫는 함수. 클라이언트 소켓과 서버 소켓을 모두 닫음
            fun close() {
                clientSocket.close()
                serverSocket.close()
            }
        }

