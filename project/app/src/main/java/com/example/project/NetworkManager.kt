import android.util.Log
import java.io.IOException
import java.io.InputStream
import java.io.OutputStream
import java.net.InetAddress
import java.net.ServerSocket
import java.net.Socket

class NetworkManager {

    private val serverPort = 7777
    private val maxBuf = 512

    private lateinit var serverSocket: ServerSocket
    private lateinit var clientSocket: Socket
    private lateinit var outputStream: OutputStream
    private lateinit var inputStream: InputStream

    fun setTCPServerSocket() {
        try {
            serverSocket = ServerSocket(serverPort)
        } catch (e: IOException) {
            Log.e("NetworkManager", "Failed to make serverSocket: ${e.message}")
            throw e
        }

    }

    fun connectToServer(ipAddress: String, port: Int) {
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

    fun close() {
        clientSocket.close()
        serverSocket.close()
    }
}