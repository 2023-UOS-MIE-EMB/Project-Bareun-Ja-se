package com.example.project.ui.home

import NetworkManager
import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import android.net.wifi.WifiConfiguration
import android.net.wifi.WifiManager
import android.net.wifi.WifiNetworkSpecifier
import android.os.Bundle
import android.util.Log
import android.view.KeyEvent
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.findNavController
import com.example.project.PacketViewModel
import com.example.project.Profile
import com.example.project.R
import com.example.project.databinding.FragmentHomeBinding
import com.example.project.ui.addprofile.AddProfileFragment.Companion.PROFILE_PREFS_KEY
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.IOException
import java.net.InetAddress
import java.net.Socket


class HomeFragment : Fragment() {

    private lateinit var packetViewModel: PacketViewModel

    private var _binding: FragmentHomeBinding? = null
    private val binding get() = _binding!!

    private lateinit var profileNameTextView: TextView
    private lateinit var profileStepTextView: TextView
    private lateinit var profileTimeTextView: TextView
    private lateinit var profileAlarmTextView: TextView


    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        val view = binding.root


        // Initialize the views
        profileNameTextView = view.findViewById(R.id.profile_name)
        profileStepTextView = view.findViewById(R.id.profile_step)
        profileTimeTextView = view.findViewById(R.id.profile_time)
        profileAlarmTextView = view.findViewById(R.id.profile_alarm)


        return view
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        packetViewModel = ViewModelProvider(requireActivity()).get(PacketViewModel::class.java)

        connectToRaspberryPiHotspot(requireActivity())

        val sharedPreferences = requireContext().getSharedPreferences(PROFILE_PREFS_KEY, Context.MODE_PRIVATE)
        val selectedProfileName = sharedPreferences.getString("selected_profile", null)
        if (selectedProfileName != null) {
            val profileJson = sharedPreferences.getString(selectedProfileName, null)
            if (profileJson != null) {
                val selectedProfile = Profile.fromJson(profileJson)
                showProfileDetails(selectedProfile)
            } else {
                Toast.makeText(requireContext(), "프로필이 없습니다. 프로필을 추가해주세요.", Toast.LENGTH_SHORT).show()
                findNavController().navigate(R.id.action_homeFragment_to_addProfileFragment)
            }
        } else {
            Toast.makeText(requireContext(), "프로필이 없습니다. 프로필을 추가해주세요.", Toast.LENGTH_SHORT).show()
            findNavController().navigate(R.id.action_homeFragment_to_addProfileFragment)
        }

        binding.addProfileButton.setOnClickListener {
            findNavController().navigate(R.id.action_homeFragment_to_addProfileFragment)
        }

        binding.changeButton.setOnClickListener {
            findNavController().navigate(R.id.action_homeFragment_to_profileListFragment)
        }

        binding.cameraOuputButton.setOnClickListener {
            packetViewModel.updateParameter1("1")
            packetViewModel.logPacketData()
        }

        binding.trunOffButton.setOnClickListener {
            packetViewModel.updateParameter2("0")
            packetViewModel.updateParameter3("10")
            packetViewModel.updateParameter4("1")
            var resultPacket: Pair<Boolean, ByteArray> = packetViewModel.makePacketToSend()
            val isSuccess: Boolean = resultPacket.first
            val dataToSend: ByteArray = resultPacket.second
            Log.d("Packet", "Data: ${packetViewModel.parsingPacket(dataToSend)}")

            if (isSuccess) {
                sendPacketToServer(dataToSend)
            } else {
                Toast.makeText(requireContext(), "패킷 생성 실패", Toast.LENGTH_SHORT).show()
            }

        }
    }
//    private var progressDialog: ProgressDialog? = null
//    private fun sendPacketToServer(packetData: ByteArray) {
//        val ipAddress = "10.42.0.1"
//        val port = 7777
//
//        progressDialog = ProgressDialog(requireContext())
//        progressDialog?.setMessage("로딩 중...") // 로딩 중 메시지 설정
//        progressDialog?.setCancelable(false) // 취소 불가능 설정
//        progressDialog?.show() // ProgressDialog 표시
//
//        CoroutineScope(Dispatchers.IO).launch {
//            val networkManager = NetworkManager()
//
//            try {
//                networkManager.setTCPServerSocket()
//                networkManager.acceptConnection()
//
//                // Send packet data to the server
//                networkManager.sendData(packetData)
//
//                val responsePacket = networkManager.receiveData()
//                Log.d("Packet", "Response: ${packetViewModel.parsingPacket(responsePacket)}")
//
//                // Close the connection
//                networkManager.close()
//
//                withContext(Dispatchers.Main) {
//                    progressDialog?.dismiss() // ProgressDialog 숨기기
//                    progressDialog = null // ProgressDialog 해제
//                }
//            } catch (e: IOException) {
//                Log.e("HomeFragment", "Failed to send packet to the server: ${e.message}")
//                withContext(Dispatchers.Main) {
//                    Toast.makeText(requireContext(), "패킷 전송 실패", Toast.LENGTH_SHORT).show()
//                    progressDialog?.dismiss() // ProgressDialog 숨기기
//                    progressDialog = null // ProgressDialog 해제
//                }
//            }
//        }
//    }
    private val networkManager = NetworkManager()
    private fun sendPacketToServer(packetData: ByteArray) {
        val ipAddress = "192.168.0.67"
        val port = 7777

        CoroutineScope(Dispatchers.IO).launch {

            try {
                networkManager.setTCPServerSocket()
                networkManager.connectToServer(ipAddress, port)

                // Send packet data to the server
                networkManager.sendData(packetData)

                val responsePacket = networkManager.receiveData()
                Log.d("Response", "Response: ${packetViewModel.parsingPacket(responsePacket)}")

                // Close the connection
                networkManager.close()
            } catch (e: IOException) {
                Log.e("HomeFragment", "Failed to send packet to the server: ${e.message}")
                withContext(Dispatchers.Main) {
                    Toast.makeText(requireContext(), "패킷 전송 실패", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }


        private var isRaspberryPiConnected = false

        private fun connectToRaspberryPiHotspot(context: Context) {
            if (isRaspberryPiConnected) {
                return // 이미 연결된 상태이면 함수를 종료합니다.
            }
        val ssid = "rpi44" // 라즈베리파이 핫스팟의 SSID를 입력합니다.
        val password = "raspberry" // 라즈베리파이 핫스팟의 비밀번호를 입력합니다.

        val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager

        val specifierBuilder = WifiNetworkSpecifier.Builder()
            .setSsid(ssid)

        if (password.isEmpty()) {
            specifierBuilder.setWpa2Passphrase("") // 비밀번호 없는 연결 설정
        } else {
            specifierBuilder.setWpa2Passphrase(password)
        }

        val specifier = specifierBuilder.build()

        val request = NetworkRequest.Builder()
            .addTransportType(NetworkCapabilities.TRANSPORT_WIFI)
            .setNetworkSpecifier(specifier)
            .build()

        val networkCallback = object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(network: Network) {

                // Wi-Fi에 성공적으로 연결되었을 때
                if (!isAdded) return

                requireActivity().runOnUiThread {
                    isRaspberryPiConnected = true
                    Toast.makeText(context, "라즈베리파이 핫스팟에 연결되었습니다.", Toast.LENGTH_SHORT).show()

                    val sharedPreferences =
                        context.getSharedPreferences(PROFILE_PREFS_KEY, Context.MODE_PRIVATE)
                    val selectedProfileName = sharedPreferences.getString("selected_profile", null)
                    if (selectedProfileName != null) {
                        val profileJson = sharedPreferences.getString(selectedProfileName, null)
                        if (profileJson != null) {
                            val selectedProfile = Profile.fromJson(profileJson)
                            showProfileDetails(selectedProfile)
                        }
                    }
                }
            }
            override fun onUnavailable() {
                super.onUnavailable()
                // Wi-Fi 연결이 불가능한 경우
                if (!isAdded) return
                requireActivity().runOnUiThread {
                    Toast.makeText(context, "라즈베리파이 핫스팟 연결에 실패했습니다.", Toast.LENGTH_SHORT).show()
                }
            }
        }

        connectivityManager.requestNetwork(request, networkCallback)
    }



    fun showProfileDetails(profile: Profile?) {
        profile?.let {
            profileNameTextView.text = it.name
            profileStepTextView.text = "최적 단계: ${it.optimalStep}"
            profileTimeTextView.text = "알람 시간(분): ${it.alarmTime}"
            profileAlarmTextView.text = "알람 방식: ${it.alarmMode}"
        }
    }

//    override fun onResume() {
//        super.onResume()
//        connectToRaspberryPiHotspot(requireActivity())
//    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}

