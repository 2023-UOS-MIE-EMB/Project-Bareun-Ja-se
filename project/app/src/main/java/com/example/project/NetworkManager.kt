import android.app.ProgressDialog
import android.content.Context
import android.util.Log
import android.widget.Toast
import com.example.project.PacketViewModel
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.IOException
import java.io.InputStream
import java.io.OutputStream
import java.net.InetAddress
import java.net.ServerSocket
import java.net.Socket

class NetworkManager {

    private val port = 7777
    private val maxBuf = 512
    private val ipAddress = "192.168.0.3"

    private lateinit var serverSocket: ServerSocket
    private lateinit var clientSocket: Socket
    private lateinit var outputStream: OutputStream
    private lateinit var inputStream: InputStream



    fun setTCPServerSocket() {
        try {
            serverSocket = ServerSocket(port)
        } catch (e: IOException) {
            Log.e("NetworkManager", "Failed to make serverSocket: ${e.message}")
            throw e
        }

    }

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

    fun sendData(data: ByteArray) {
        try {
            outputStream.write(data)
            outputStream.flush()
        } catch (e: IOException) {
            Log.e("NetworkManager", "Failed to receiveData: ${e.message}")
            throw e
        }
    }

    fun sendPacketToServer(
        packetData: ByteArray,
        packetViewModel: PacketViewModel,
        context: Context
    ) {
        CoroutineScope(Dispatchers.IO).launch {
            var progressDialog: ProgressDialog? = null

            try {
                withContext(Dispatchers.Main) {
                    // 진행 대화상자 표시
                    progressDialog = ProgressDialog(context)
                    progressDialog?.setMessage("로딩중...")
                    progressDialog?.setCancelable(false)
                    progressDialog?.show()
                }
                setTCPServerSocket()
                connectToServer()

                // Send packet data to the server
                sendData(packetData)

                val responsePacket = receiveData()
                Log.d("Response", "Response: ${packetViewModel.parsingPacket(responsePacket)}")

                // Close the connection
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

    //streaming
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

                // Send packet data to the server
                sendData(packetData)

                val responsePacket = receiveData()
                Log.d("Response", "Response: ${packetViewModel.parsingPacket(responsePacket)}")

                // Close the connection
                close()

                // Callback with responsePacket data
                callback(responsePacket)
            } catch (e: IOException) {
                Log.e("NetworkManager", "Failed to send packet to the server: ${e.message}")
                withContext(Dispatchers.Main) {
                    Toast.makeText(requireContext(), "패킷 전송 실패", Toast.LENGTH_SHORT).show()
                }

                // Callback with null to indicate failure
                callback(null)
            }
        }
    }





            fun close() {
                clientSocket.close()
                serverSocket.close()
            }
        }

