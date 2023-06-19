package com.example.project.ui.streaming

import NetworkManager
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.webkit.WebView
import android.widget.Button
import android.widget.ProgressBar
import android.widget.Toast
import com.example.project.R
import com.example.project.Streaming
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.findNavController
import com.example.project.PacketViewModel

// 기능 : 스트리밍 화면을 표시하고 관리하는 프래그먼트
class StreamingFragment : Fragment() {
    private lateinit var webView: WebView
    private lateinit var closeButton: Button
    private lateinit var streaming: Streaming
    private lateinit var packetViewModel: PacketViewModel
    private lateinit var progressBar: ProgressBar
    private val networkManager = NetworkManager()

    // 기능 : 프래그먼트의 화면을 생성하고 변수들을 초기화하는 매서드
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_streaming, container, false)

        webView = view.findViewById(R.id.WebView)
        closeButton = view.findViewById(R.id.closeButton)
        progressBar = view.findViewById(R.id.Progressbar)
        streaming = Streaming(webView, progressBar)

        // 기능 : closeButton을 누르는 경우 스트리밍을 중지하고 스트리밍 요청 인자를 0(사용안함)으로 업데이트한 후 해당 값 서버로 패킷 송신
        closeButton.setOnClickListener {
            streaming.stopStreaming()
            packetViewModel.updateParameter1("0")
            var resultPacket: Pair<Boolean, ByteArray> = packetViewModel.makePacketToSend()
            val isSuccess: Boolean = resultPacket.first
            val dataToSend: ByteArray = resultPacket.second
            if (isSuccess) {
                networkManager.sendPacketToServer(dataToSend, packetViewModel, requireContext())
            } else {
                Toast.makeText(requireContext(), "패킷 생성 실패", Toast.LENGTH_SHORT).show()
            }

            findNavController().popBackStack()
        }

        return view
    }

    // 기능 : 화면이 생성된 후 호출되는 메서드. 스트리밍을 요청 인자를 1(사용)으로 업데이트 한 후 서버로 패킷 송신. 성공한 경우 받은 응답 패킷으로 스트리밍 시작
   override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        packetViewModel = ViewModelProvider(requireActivity()).get(PacketViewModel::class.java)

        packetViewModel.updateParameter1("1")
        var resultPacket: Pair<Boolean, ByteArray> = packetViewModel.makePacketToSend()
        val isSuccess: Boolean = resultPacket.first
        val dataToSend: ByteArray = resultPacket.second

        Log.d("Packet", "Data: ${packetViewModel.parsingPacket(dataToSend)}")

        if (isSuccess) {
            networkManager.sendPacketToServer2(
                dataToSend,
                packetViewModel,
                { requireContext() }) { responsePacket ->
                if (isAdded) { // 프래그먼트가 액티비티에 연결되어 있는지 확인
                    requireActivity().runOnUiThread {
                        if (responsePacket != null) {
                            streaming.parsePacketAndStartStreaming(responsePacket)
                        } else {
                            Toast.makeText(requireContext(), "패킷 생성 실패", Toast.LENGTH_SHORT).show()
                        }
                    }
                }
            }
        }
    }

    // 기능 : 창을 닫는 경우 호출되는 메서드. 스트리밍을 중지함
    override fun onDestroyView() {
        super.onDestroyView()
        streaming.stopStreaming()
    }

}