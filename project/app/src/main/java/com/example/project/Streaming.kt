package com.example.project

import android.media.MediaPlayer
import android.net.Uri
import android.util.Log
import android.view.View
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.VideoView
import org.json.JSONObject
import android.widget.MediaController
import android.widget.ProgressBar

class Streaming(private val webView: WebView, private val progressBar: ProgressBar) {
    private var mediaPlayer: MediaPlayer? = null

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
                Log.d("ADDRESS", "Streaming Address: $streamingAddr") // 주소 데이터 로그 출력
                startStreaming(streamingAddr)
                progressBar.visibility = View.GONE
            }
        }
    }

    private fun extractStreamingAddress(jsonData: String): String {
        val jsonObject = JSONObject(jsonData)
        return jsonObject.optString("5")
    }

    fun startStreaming(streamingUrl: String) {

        webView.loadUrl(streamingUrl)
    }

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
