package com.example.project

import android.media.MediaPlayer
import android.util.Log
import android.view.View
import android.webkit.WebView
import org.json.JSONObject
import android.widget.ProgressBar

// 기능 : 스트리밍을 위한 클래스, 받은 패킷을 파싱하고 스트리밍을 진행하는 메서드가 있음

class Streaming(private val webView: WebView, private val progressBar: ProgressBar) {
    private var mediaPlayer: MediaPlayer? = null

    // 기능 : 패킷을 문자열로 변환한 후, 헤더 정보를 추출하여 스트리밍 주소를 얻고, 해당 주소로 스트리밍을 시작
    fun parsePacketAndStartStreaming(packet: ByteArray) {
        val packetString = String(packet, Charsets.UTF_8)
        val lines = packetString.split("\r\n")

        if (lines.isNotEmpty()) {
            val headerLine = lines[0]
            val headerValues = headerLine.split(":")
            val headerKey = headerValues[0]
            val headerValue = headerValues[1]

            if (headerKey == "H") {
                val bodyLine = lines[1]
                val jsonData = bodyLine.substring(0, headerValue.toInt())

                val streamingAddr = extractStreamingAddress(jsonData)
                Log.d("ADDRESS", "Streaming Address: $streamingAddr")
                startStreaming(streamingAddr)
                progressBar.visibility = View.GONE
            }
        }
    }
    // 기능 : JSON 데이터에서 스트리밍 주소를 추출
    fun extractStreamingAddress(jsonData: String): String {
        val jsonObject = JSONObject(jsonData)
        return jsonObject.optString("5")
    }

    // 기능 : 주어진 스트리밍 주소를 사용하여 스트리밍을 시작
    fun startStreaming(streamingUrl: String) {

        webView.loadUrl(streamingUrl)
    }

    // 기능 : 스트리밍을 중지하는 함수. WebView의 로딩을 중지하고, MediaPlayer를 해제하여 리소스를 해제
    fun stopStreaming() {
        webView.stopLoading()
        mediaPlayer?.let { player ->
            player.stop()
            player.reset()
            player.release()
        }
        mediaPlayer = null
    }
}
