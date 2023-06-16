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


class StreamingFragment : Fragment() {
    private lateinit var webView: WebView
    private lateinit var closeButton: Button
    private lateinit var streaming: Streaming
    private lateinit var packetViewModel: PacketViewModel
    private lateinit var progressBar: ProgressBar
    private val networkManager = NetworkManager()

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

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        packetViewModel = ViewModelProvider(requireActivity()).get(PacketViewModel::class.java)
        //val streamingaddress =  "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
        //streaming.startStreaming2(streamingaddress)
        //if (packetViewModel.checkIfP3P4Changed() == 1) {
            // p3 또는 p4 값이 변경되었을 때의 처리
        packetViewModel.updateParameter1("1")
        var resultPacket: Pair<Boolean, ByteArray> = packetViewModel.makePacketToSend()
        val isSuccess: Boolean = resultPacket.first
        val dataToSend: ByteArray = resultPacket.second

        Log.d("Packet", "Data: ${packetViewModel.parsingPacket(dataToSend)}")

//            if (isSuccess) {
//                networkManager.sendPacketToServer2(dataToSend, packetViewModel, { requireContext() }) { responsePacket ->
//                    requireActivity().runOnUiThread {
//                        if (responsePacket != null) {
//                            // responsePacket을 사용하여 원하는 작업 수행
//                            streaming.parsePacketAndStartStreaming(responsePacket)
//                        } else {
//                            // 패킷 전송 실패 처리
//                        }
//                    }
//                }
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


    override fun onDestroyView() {
        super.onDestroyView()
        streaming.stopStreaming()
    }

}