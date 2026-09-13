package com.example.ieltsbygama

import android.Manifest
import android.annotation.SuppressLint
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import android.util.Log
import android.webkit.JavascriptInterface
import android.webkit.PermissionRequest
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.OnBackPressedCallback
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import android.graphics.Color
import android.view.ViewGroup
import android.widget.FrameLayout
import java.util.Locale

class MainActivity : ComponentActivity(), TextToSpeech.OnInitListener {

    private lateinit var webView: WebView
    private var textToSpeech: TextToSpeech? = null
    private var isTtsReady = false
    private var speechRecognizer: SpeechRecognizer? = null
    private val mainHandler = Handler(Looper.getMainLooper())

    companion object {
        private const val TAG = "IELTS_GAMA_AUDIO"
        private const val PERMISSION_REQUEST_RECORD_AUDIO = 201
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Initialize Android Native Text-to-Speech Engine
        textToSpeech = TextToSpeech(applicationContext, this)

        // Request RECORD_AUDIO runtime permission proactively
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.RECORD_AUDIO),
                PERMISSION_REQUEST_RECORD_AUDIO
            )
        }

        webView = WebView(this).apply {
            settings.apply {
                javaScriptEnabled = true
                domStorageEnabled = true
                allowFileAccess = true
                allowContentAccess = true
                mediaPlaybackRequiresUserGesture = false
                cacheMode = WebSettings.LOAD_DEFAULT
                useWideViewPort = true
                loadWithOverviewMode = true
                builtInZoomControls = false
                displayZoomControls = false
            }

            webViewClient = object : WebViewClient() {
                override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
                    return false
                }
            }

            webChromeClient = object : WebChromeClient() {
                override fun onPermissionRequest(request: PermissionRequest?) {
                    request?.grant(request.resources)
                }
            }

            // Expose native Android audio capabilities to JavaScript
            addJavascriptInterface(AndroidTTSBridge(), "AndroidTTS")
            addJavascriptInterface(AndroidSTTBridge(), "AndroidSTT")
        }

        // Set dark status bar and navigation bar with white icons
        window.statusBarColor = Color.parseColor("#161e2b")
        window.navigationBarColor = Color.parseColor("#0f141c")
        val insetsController = WindowCompat.getInsetsController(window, window.decorView)
        insetsController.isAppearanceLightStatusBars = false
        insetsController.isAppearanceLightNavigationBars = false

        val initialStatusHeight = getStatusBarHeight()
        val rootContainer = FrameLayout(this).apply {
            layoutParams = ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT
            )
            setBackgroundColor(Color.parseColor("#161e2b"))
            setPadding(0, initialStatusHeight, 0, 0)
            addView(webView, FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.MATCH_PARENT
            ))
        }

        setContentView(rootContainer)

        // Handle edge-to-edge system bar and camera cutout insets
        ViewCompat.setOnApplyWindowInsetsListener(rootContainer) { view, insets ->
            val insetsType = WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.displayCutout()
            val bars = insets.getInsets(insetsType)
            val topPadding = maxOf(bars.top, initialStatusHeight)
            view.setPadding(bars.left, topPadding, bars.right, bars.bottom)
            insets
        }

        // Handle Back button navigation inside WebView
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (webView.canGoBack()) {
                    webView.goBack()
                } else {
                    isEnabled = false
                    onBackPressedDispatcher.onBackPressed()
                }
            }
        })

        // Initialize SpeechRecognizer on Main UI Thread
        initSpeechRecognizer()

        // Load self-contained offline curriculum & responsive UI
        webView.loadUrl("file:///android_asset/www/index.html")
    }

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            val result = textToSpeech?.setLanguage(Locale.US)
            isTtsReady = result != TextToSpeech.LANG_MISSING_DATA && result != TextToSpeech.LANG_NOT_SUPPORTED
            Log.d(TAG, "TextToSpeech initialized successfully, ready: $isTtsReady")
            if (isTtsReady) {
                textToSpeech?.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
                    override fun onStart(utteranceId: String?) {
                        evaluateJs("if (window.onTTSStarted) window.onTTSStarted('$utteranceId');")
                    }
                    override fun onDone(utteranceId: String?) {
                        evaluateJs("if (window.onTTSFinished) window.onTTSFinished('$utteranceId');")
                    }
                    override fun onError(utteranceId: String?) {
                        evaluateJs("if (window.onTTSError) window.onTTSError('$utteranceId');")
                    }
                })
            }
        } else {
            Log.e(TAG, "TextToSpeech init failed with status: $status")
        }
    }

    private fun initSpeechRecognizer() {
        mainHandler.post {
            if (SpeechRecognizer.isRecognitionAvailable(this)) {
                speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this).apply {
                    setRecognitionListener(object : RecognitionListener {
                        override fun onReadyForSpeech(params: Bundle?) {
                            evaluateJs("if (window.onSpeechReady) window.onSpeechReady();")
                        }
                        override fun onBeginningOfSpeech() {
                            evaluateJs("if (window.onSpeechBegin) window.onSpeechBegin();")
                        }
                        override fun onRmsChanged(rmsdB: Float) {}
                        override fun onBufferReceived(buffer: ByteArray?) {}
                        override fun onEndOfSpeech() {
                            evaluateJs("if (window.onSpeechEnd) window.onSpeechEnd();")
                        }
                        override fun onError(error: Int) {
                            Log.w(TAG, "SpeechRecognizer error code: $error")
                            evaluateJs("if (window.onSpeechError) window.onSpeechError($error);")
                        }
                        override fun onResults(results: Bundle?) {
                            val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                            if (!matches.isNullOrEmpty()) {
                                val transcript = matches[0].replace("'", "\\'").replace("\n", " ")
                                evaluateJs("if (window.onAndroidSpeechResult) window.onAndroidSpeechResult('$transcript');")
                            }
                        }
                        override fun onPartialResults(partialResults: Bundle?) {
                            val matches = partialResults?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                            if (!matches.isNullOrEmpty()) {
                                val transcript = matches[0].replace("'", "\\'").replace("\n", " ")
                                evaluateJs("if (window.onAndroidSpeechPartial) window.onAndroidSpeechPartial('$transcript');")
                            }
                        }
                        override fun onEvent(eventType: Int, params: Bundle?) {}
                    })
                }
            }
        }
    }

    private fun evaluateJs(script: String) {
        mainHandler.post {
            webView.evaluateJavascript(script, null)
        }
    }

    private fun getStatusBarHeight(): Int {
        val resourceId = resources.getIdentifier("status_bar_height", "dimen", "android")
        return if (resourceId > 0) resources.getDimensionPixelSize(resourceId) else 0
    }

    // Native Text-To-Speech JavaScript Interface
    inner class AndroidTTSBridge {

        @JavascriptInterface
        fun speak(text: String) {
            speak(text, "ielts_tts")
        }

        @JavascriptInterface
        fun speak(text: String, utteranceId: String) {
            Log.d(TAG, "TTS speak requested: ${text.take(60)}...")
            val clean = text.replace(Regex("[#*_>`•\\[\\]]"), " ")
                .replace(Regex("\\s+"), " ")
                .trim()

            mainHandler.post {
                if (textToSpeech == null) {
                    textToSpeech = TextToSpeech(applicationContext, this@MainActivity)
                }
                
                // Chunk long passages so Android TTS never overflows buffer
                val chunks = clean.chunked(1200)
                chunks.forEachIndexed { index, chunk ->
                    val queueMode = if (index == 0) TextToSpeech.QUEUE_FLUSH else TextToSpeech.QUEUE_ADD
                    textToSpeech?.speak(chunk, queueMode, null, "${utteranceId}_$index")
                }
            }
        }

        @JavascriptInterface
        fun stop() {
            mainHandler.post {
                textToSpeech?.stop()
            }
        }

        @JavascriptInterface
        fun isSpeaking(): Boolean {
            return textToSpeech?.isSpeaking ?: false
        }

        @JavascriptInterface
        fun isAvailable(): Boolean {
            return isTtsReady || textToSpeech != null
        }
    }

    // Native Speech-To-Text JavaScript Interface
    inner class AndroidSTTBridge {
        @JavascriptInterface
        fun startListening() {
            mainHandler.post {
                if (ContextCompat.checkSelfPermission(this@MainActivity, Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED) {
                    val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                        putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                        putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.US.toString())
                        putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)
                        putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 3)
                    }
                    try {
                        speechRecognizer?.startListening(intent)
                    } catch (e: Exception) {
                        Log.e(TAG, "Error starting speech recognition: ${e.message}")
                        evaluateJs("if (window.onSpeechError) window.onSpeechError(-1);")
                    }
                } else {
                    ActivityCompat.requestPermissions(
                        this@MainActivity,
                        arrayOf(Manifest.permission.RECORD_AUDIO),
                        PERMISSION_REQUEST_RECORD_AUDIO
                    )
                }
            }
        }

        @JavascriptInterface
        fun stopListening() {
            mainHandler.post {
                try {
                    speechRecognizer?.stopListening()
                } catch (e: Exception) {
                    // Ignore
                }
            }
        }

        @JavascriptInterface
        fun isAvailable(): Boolean {
            return SpeechRecognizer.isRecognitionAvailable(this@MainActivity)
        }
    }

    override fun onResume() {
        super.onResume()
        webView.onResume()
    }

    override fun onPause() {
        super.onPause()
        webView.onPause()
        textToSpeech?.stop()
    }

    override fun onDestroy() {
        textToSpeech?.stop()
        textToSpeech?.shutdown()
        speechRecognizer?.destroy()
        webView.destroy()
        super.onDestroy()
    }
}
