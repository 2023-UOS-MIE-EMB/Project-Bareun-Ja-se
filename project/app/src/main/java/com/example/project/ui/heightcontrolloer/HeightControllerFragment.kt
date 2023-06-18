package com.example.project.ui.heightcontrolloer

import NetworkManager
import android.app.ProgressDialog
import android.content.Context
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.example.project.Profile
import com.example.project.databinding.FragmentHeightcontrollerBinding
import androidx.lifecycle.ViewModelProvider
import com.example.project.FirstLaunch
import com.example.project.PacketViewModel
import com.example.project.SharedData
import com.example.project.ui.addprofile.AddProfileFragment
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.IOException

class HeightControllerFragment : Fragment() {

    private lateinit var packetViewModel: PacketViewModel
    private val networkManager = NetworkManager()

    private var _binding: FragmentHeightcontrollerBinding? = null
    private val binding get() = _binding!!

    private var currentStep = 0
        set(value) {
            field = value
            updateNowStepText(currentStep)
        }


    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentHeightcontrollerBinding.inflate(inflater, container, false)

        packetViewModel = ViewModelProvider(requireActivity()).get(PacketViewModel::class.java)
        var resultPacket: Pair<Boolean, ByteArray> = packetViewModel.makePacketToSend()
        val isSuccess: Boolean = resultPacket.first
        val dataToSend: ByteArray = resultPacket.second

        sendPacketToServer3(dataToSend, packetViewModel, requireContext())

//        val sharedPreferences = requireContext().getSharedPreferences(AddProfileFragment.PROFILE_PREFS_KEY, Context.MODE_PRIVATE)
//        val selectedProfileName = sharedPreferences.getString("selected_profile", null)
//        if (selectedProfileName != null) {
//            val profileJson = sharedPreferences.getString(selectedProfileName, null)
//            if (profileJson != null) {
//                val selectedProfile = Profile.fromJson(profileJson)
//                if (SharedData.firstLaunch.heightFirstLaunch && selectedProfile != null) {
//                    if (selectedProfile.optimalStep != "미설정") {
//                        currentStep = selectedProfile.optimalStep.toInt()
//                    }
//                    else{
//                        currentStep = 0
//                    }
//                    SharedData.firstLaunch.heightFirstLaunch = false
//                }
//                updateNowStepText()
//            }
//        }




        binding.stepInputButton.setOnClickListener {
            val inputText = binding.stepEdittext.text.toString()
            if (inputText.isNotEmpty()) {
                val step = inputText.toIntOrNull()
                if (step != null && step in 1..20) {
                    currentStep = step
                    updateNowStepText(currentStep)
                    binding.stepEdittext.text = null
                    packetViewModel.updateParameter0(currentStep.toString())
                    var resultPacket: Pair<Boolean, ByteArray> = packetViewModel.makePacketToSend()
                    val isSuccess: Boolean = resultPacket.first
                    val dataToSend: ByteArray = resultPacket.second
                    Log.d("Packet", "Data: ${packetViewModel.parsingPacket(dataToSend)}")

                    if (isSuccess) {
                        networkManager.sendPacketToServer(dataToSend, packetViewModel, requireContext())
                    } else {
                        Toast.makeText(requireContext(), "패킷 생성 실패", Toast.LENGTH_SHORT).show()
                    }
                } else {
                    Toast.makeText(requireContext(), "입력 값은 1에서 20 사이로 입력해주세요.", Toast.LENGTH_SHORT).show()
                }
            }
        }

        binding.stepUpButton.setOnClickListener {
            if (currentStep < 20) {
                currentStep++
                updateNowStepText(currentStep)
                packetViewModel.updateParameter0(currentStep.toString())
                var resultPacket: Pair<Boolean, ByteArray> = packetViewModel.makePacketToSend()
                val isSuccess: Boolean = resultPacket.first
                val dataToSend: ByteArray = resultPacket.second
                Log.d("Packet", "Data: ${packetViewModel.parsingPacket(dataToSend)}")

                if (isSuccess) {
                    networkManager.sendPacketToServer(dataToSend, packetViewModel, requireContext())
                } else {
                    Toast.makeText(requireContext(), "패킷 생성 실패", Toast.LENGTH_SHORT).show()
                }
            }
        }

        binding.stepDownButton.setOnClickListener {
            if (currentStep > 1) {
                currentStep--
                updateNowStepText(currentStep)
                packetViewModel.updateParameter0(currentStep.toString())
                var resultPacket: Pair<Boolean, ByteArray> = packetViewModel.makePacketToSend()
                val isSuccess: Boolean = resultPacket.first
                val dataToSend: ByteArray = resultPacket.second
                Log.d("Packet", "Data: ${packetViewModel.parsingPacket(dataToSend)}")

                if (isSuccess) {
                    networkManager.sendPacketToServer(dataToSend, packetViewModel, requireContext())
                } else {
                    Toast.makeText(requireContext(), "패킷 생성 실패", Toast.LENGTH_SHORT).show()
                }
            }
        }

        binding.saveButton.setOnClickListener {
            val selectedProfileName = packetViewModel.getSelectedProfileName(requireContext())
            if (selectedProfileName != null) {
                val profileJson = packetViewModel.getProfileJson(requireContext(), selectedProfileName)
                if (profileJson != null) {
                    var profile = Profile.fromJson(profileJson)
                    profile?.let {
                        it.optimalStep = currentStep.toString()
                        packetViewModel.saveProfile(requireContext(), it)
                        Toast.makeText(requireContext(), "현재 단계가 저장되었습니다.", Toast.LENGTH_SHORT)
                            .show()
                    }
                }
            }
        }

//        if (savedInstanceState != null) {
//            currentStep = savedInstanceState.getInt("currentStep", 0)
//            updateNowStepText()
//        }

        return binding.root
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putInt("currentStep", currentStep)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    private fun sendPacketToServer3(
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
                networkManager.setTCPServerSocket()
                networkManager.connectToServer()

                // Send packet data to the server
                networkManager.sendData(packetData)

                val responsePacket = networkManager.receiveData()
                Log.d("Response", "Response: ${packetViewModel.parsingPacket(responsePacket)}")

                val extractedValue = extractExistingStep(responsePacket)
                if (extractedValue != null) {
                    // Perform the desired action with the extracted value (e.g., update current step)
                    val currentStep = extractedValue.toIntOrNull()
                    if (currentStep != null) {
                        withContext(Dispatchers.Main) {
                            // Update the current step and UI
                            this@HeightControllerFragment.currentStep = currentStep
                        }
                    }
                }

                // Close the connection
                networkManager.close()
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

    private fun extractExistingStep(packet: ByteArray): String? {
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
                val jsonObject = JSONObject(jsonData)
                return jsonObject.optString("6")
            }
        }
        return null
    }

    private fun updateNowStepText(currentStep: Int) {
        binding.nowStep.text = currentStep.toString()
        binding.nowStep.invalidate()
    }

}