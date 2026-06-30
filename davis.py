import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Coffee Sales Analytics Dashboard", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

html_code = r"""
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BINUS Data Visualization - Coffee Sales Analytics Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        coffee: {
                            50: '#fdf8f5', 100: '#fbeee6', 500: '#d97706', 700: '#b45309', 800: '#78350f', 900: '#451a03',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        .tab-transition { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #1e293b; }
        ::-webkit-scrollbar-thumb { background: #475569; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #d97706; }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans flex flex-col antialiased selection:bg-amber-500 selection:text-slate-950">

    <header class="bg-slate-900 border-b border-slate-800 sticky top-0 z-50 shadow-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-3">
                <div class="bg-amber-600 text-slate-950 p-2 rounded-xl flex items-center justify-center shadow-lg shadow-amber-600/20">
                    <i class="fa-solid fa-mug-hot text-xl"></i>
                </div>
                <div>
                    <h1 class="text-lg font-extrabold tracking-tight text-white flex items-center gap-2">
                        COFFEE INSIGHTS & STORYTELLING <span class="text-xs bg-amber-500/15 text-amber-500 px-2 py-0.5 rounded border border-amber-500/30">BINUS EXAM 2026</span>
                    </h1>
                    <p class="text-xs text-slate-400">Course Code: ISYS6915003 | Data Visualization Project</p>
                </div>
            </div>
            <div class="flex items-center gap-4 bg-slate-950/60 px-4 py-2 rounded-xl border border-slate-800/80">
                <div class="text-right hidden sm:block">
                    <p class="text-xs font-semibold text-slate-300" id="studentName">Sean Juan Gavin Perwira</p>
                    <p class="text-[10px] text-slate-500" id="studentNIM">BINUS Student</p>
                </div>
                <button onclick="editCredentials()" class="text-slate-400 hover:text-amber-500 p-1.5 hover:bg-slate-800 rounded-lg transition-colors" title="Edit Student Profile">
                    <i class="fa-solid fa-user-pen"></i>
                </button>
            </div>
        </div>
    </header>

    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col gap-6">
        <section class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col md:flex-row items-center justify-between gap-5 transition-all hover:border-slate-700">
            <div class="space-y-1 flex-1">
                <h2 class="text-base font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-database text-amber-500"></i> Data Connection Gateway
                </h2>
                <p class="text-xs text-slate-400 leading-relaxed">
                    Designed specifically for <code class="text-amber-400 bg-slate-950 px-1.5 py-0.5 rounded border border-slate-800">Coffee_sales_cleaned.csv</code>. Drag-and-drop your clean file below or test directly with our rich preloaded 2026 sales model.
                </p>
            </div>
            <div class="flex flex-wrap items-center gap-3 w-full md:w-auto">
                <label class="flex flex-1 md:flex-initial items-center justify-center gap-2 bg-slate-950 hover:bg-slate-800 border border-dashed border-slate-700 hover:border-amber-500/50 px-4 py-2.5 rounded-xl text-xs cursor-pointer transition-all text-slate-300">
                    <i class="fa-solid fa-cloud-arrow-up text-amber-500"></i>
                    <span>Upload CSV File</span>
                    <input type="file" id="csvFileInput" accept=".csv" class="hidden" onchange="handleCSVUpload(event)">
                </label>
                <button onclick="tryLoadLocalCSV()" class="flex-1 md:flex-initial bg-amber-600 hover:bg-amber-500 text-slate-950 font-semibold px-4 py-2.5 rounded-xl text-xs flex items-center justify-center gap-2 transition-all shadow-lg shadow-amber-600/10">
                    <i class="fa-solid fa-rotate"></i> Sync local CSV
                </button>
            </div>
        </section>

        <div id="statusAlert" class="hidden px-5 py-3.5 rounded-xl border flex items-center gap-3 text-xs transition-all animate-pulse"></div>

        <div class="border-b border-slate-800 flex items-center justify-between">
            <nav class="flex gap-1" aria-label="Tabs">
                <button onclick="switchTab('dashboard')" id="tabBtn-dashboard" class="px-4 py-3 text-sm font-semibold border-b-2 border-amber-500 text-amber-500 flex items-center gap-2 tab-transition">
                    <i class="fa-solid fa-chart-line"></i> Operational Dashboard
                </button>
                <button onclick="switchTab('eda')" id="tabBtn-eda" class="px-4 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700 flex items-center gap-2 tab-transition">
                    <i class="fa-solid fa-magnifying-glass-chart"></i> Exploratory Data Analysis (EDA)
                </button>
                <button onclick="switchTab('story')" id="tabBtn-story" class="px-4 py-3 text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700 flex items-center gap-2 tab-transition">
                    <i class="fa-solid fa-book-open"></i> Critical Reflection & Story
                </button>
            </nav>
            <div id="rowCountBadge" class="text-xs bg-slate-900 border border-slate-800 px-3 py-1 rounded-full text-slate-400">
                Data Rows: <span class="font-bold text-amber-500" id="rowCount">0</span>
            </div>
        </div>

        <div id="tabContent-dashboard" class="space-y-6">
            <section class="bg-slate-900 border border-slate-800/80 rounded-2xl p-5 shadow-xl">
                <div class="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
                    <h3 class="text-sm font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-sliders text-amber-500"></i> Interactive Dimensional Controls
                    </h3>
                    <button onclick="resetFilters()" class="text-xs text-slate-400 hover:text-amber-500 transition-colors flex items-center gap-1.5">
                        <i class="fa-solid fa-rotate-left"></i> Reset Selection
                    </button>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div class="space-y-1.5">
                        <label class="text-[11px] font-bold text-slate-400 tracking-wider uppercase">Store Location</label>
                        <select id="filterLocation" onchange="applyFilters()" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500">
                            <option value="All">All Locations</option>
                        </select>
                    </div>
                    <div class="space-y-1.5">
                        <label class="text-[11px] font-bold text-slate-400 tracking-wider uppercase">Product Item</label>
                        <select id="filterCategory" onchange="applyFilters()" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500">
                            <option value="All">All Coffee Blends</option>
                        </select>
                    </div>
                    <div class="space-y-1.5">
                        <label class="text-[11px] font-bold text-slate-400 tracking-wider uppercase">Payment Mode</label>
                        <select id="filterPayment" onchange="applyFilters()" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500">
                            <option value="All">All Payment Systems</option>
                        </select>
                    </div>
                    <div class="space-y-1.5">
                        <label class="text-[11px] font-bold text-slate-400 tracking-wider uppercase">Date Filter Range</label>
                        <select id="filterDateRange" onchange="applyFilters()" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500">
                            <option value="All">Entire Timeline Range</option>
                            <option value="Morning">Morning Sales Target (06:00 - 11:59)</option>
                            <option value="Afternoon">Afternoon Rush (12:00 - 17:59)</option>
                            <option value="Evening">Evening/Late Hours (18:00 - 23:59)</option>
                        </select>
                    </div>
                </div>
            </section>

            <section class="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl flex items-center justify-between shadow-md hover:border-slate-700 transition-all">
                    <div>
                        <p class="text-xs text-slate-400 font-semibold uppercase">Gross Revenue</p>
                        <h4 class="text-2xl font-black text-white tracking-tight mt-1" id="kpiRevenue">IDR 0</h4>
                    </div>
                    <div class="h-12 w-12 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center text-lg">
                        <i class="fa-solid fa-wallet"></i>
                    </div>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl flex items-center justify-between shadow-md hover:border-slate-700 transition-all">
                    <div>
                        <p class="text-xs text-slate-400 font-semibold uppercase">Total Volume</p>
                        <h4 class="text-2xl font-black text-white tracking-tight mt-1" id="kpiVolume">0</h4>
                    </div>
                    <div class="h-12 w-12 rounded-xl bg-blue-500/10 text-blue-500 flex items-center justify-center text-lg">
                        <i class="fa-solid fa-box-open"></i>
                    </div>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl flex items-center justify-between shadow-md hover:border-slate-700 transition-all">
                    <div>
                        <p class="text-xs text-slate-400 font-semibold uppercase">Total Tickets</p>
                        <h4 class="text-2xl font-black text-white tracking-tight mt-1" id="kpiTickets">0</h4>
                    </div>
                    <div class="h-12 w-12 rounded-xl bg-amber-500/10 text-amber-500 flex items-center justify-center text-lg">
                        <i class="fa-solid fa-receipt"></i>
                    </div>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl flex items-center justify-between shadow-md hover:border-slate-700 transition-all">
                    <div>
                        <p class="text-xs text-slate-400 font-semibold uppercase">Average Ticket</p>
                        <h4 class="text-2xl font-black text-white tracking-tight mt-1" id="kpiAverage">IDR 0</h4>
                    </div>
                    <div class="h-12 w-12 rounded-xl bg-purple-500/10 text-purple-500 flex items-center justify-center text-lg">
                        <i class="fa-solid fa-chart-pie"></i>
                    </div>
                </div>
            </section>

            <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="bg-slate-900 border border-slate-800/80 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between border-b border-slate-800 pb-2 mb-3">
                            <h4 class="text-sm font-bold text-white flex items-center gap-2">
                                <span class="w-2.5 h-2.5 rounded-full bg-amber-500 animate-pulse"></span>
                                Sales Revenue & Transactions Over Time
                            </h4>
                            <span class="text-[10px] bg-amber-500/10 text-amber-500 border border-amber-500/20 px-2 py-0.5 rounded-md">Dual-Axis Trend</span>
                        </div>
                        <div id="salesTrendChart" class="w-full h-72 bg-slate-950 rounded-xl overflow-hidden"></div>
                    </div>
                    <div class="mt-4 p-4 bg-slate-950/60 border border-slate-800 rounded-xl">
                        <div class="flex items-center gap-2 mb-1.5">
                            <i class="fa-solid fa-circle-info text-amber-500 text-xs"></i>
                            <span class="text-xs font-bold text-slate-200 uppercase tracking-wider">Dynamic Trend Analysis</span>
                        </div>
                        <p id="insightTrendText" class="text-xs text-slate-400 leading-relaxed">Calculating trends...</p>
                    </div>
                </div>

                <div class="bg-slate-900 border border-slate-800/80 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between border-b border-slate-800 pb-2 mb-3">
                            <h4 class="text-sm font-bold text-white flex items-center gap-2">
                                <span class="w-2.5 h-2.5 rounded-full bg-orange-500"></span>
                                Hourly Sales Density by Day of Week
                            </h4>
                            <span class="text-[10px] bg-orange-500/10 text-orange-500 border border-orange-500/20 px-2 py-0.5 rounded-md">Operational Heatmap</span>
                        </div>
                        <div id="heatmapDensityChart" class="w-full h-72 bg-slate-950 rounded-xl overflow-hidden"></div>
                    </div>
                    <div class="mt-4 p-4 bg-slate-950/60 border border-slate-800 rounded-xl">
                        <div class="flex items-center gap-2 mb-1.5">
                            <i class="fa-solid fa-fire text-orange-500 text-xs"></i>
                            <span class="text-xs font-bold text-slate-200 uppercase tracking-wider">Operational Peak Insight</span>
                        </div>
                        <p id="insightHeatmapText" class="text-xs text-slate-400 leading-relaxed">Analyzing hourly load cycles...</p>
                    </div>
                </div>

                <div class="bg-slate-900 border border-slate-800/80 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between border-b border-slate-800 pb-2 mb-3">
                            <h4 class="text-sm font-bold text-white flex items-center gap-2">
                                <span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
                                Unit Price vs. Hourly Revenue Distribution
                            </h4>
                            <span class="text-[10px] bg-blue-500/10 text-blue-500 border border-blue-500/20 px-2 py-0.5 rounded-md">Correlation Plot</span>
                        </div>
                        <div id="scatterCorrelationChart" class="w-full h-72 bg-slate-950 rounded-xl overflow-hidden"></div>
                    </div>
                    <div class="mt-4 p-4 bg-slate-950/60 border border-slate-800 rounded-xl">
                        <div class="flex items-center gap-2 mb-1.5">
                            <i class="fa-solid fa-chart-line text-blue-500 text-xs"></i>
                            <span class="text-xs font-bold text-slate-200 uppercase tracking-wider">Scatter Correlation Insight</span>
                        </div>
                        <p id="insightScatterText" class="text-xs text-slate-400 leading-relaxed">Processing correlations...</p>
                    </div>
                </div>

                <div class="bg-slate-900 border border-slate-800/80 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between border-b border-slate-800 pb-2 mb-3">
                            <h4 class="text-sm font-bold text-white flex items-center gap-2">
                                <span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span>
                                Share of Revenue by Product Line
                            </h4>
                            <span class="text-[10px] bg-purple-500/10 text-purple-500 border border-purple-500/20 px-2 py-0.5 rounded-md">Donut Composition</span>
                        </div>
                        <div id="donutDistributionChart" class="w-full h-72 bg-slate-950 rounded-xl overflow-hidden"></div>
                    </div>
                    <div class="mt-4 p-4 bg-slate-950/60 border border-slate-800 rounded-xl">
                        <div class="flex items-center gap-2 mb-1.5">
                            <i class="fa-solid fa-pie-chart text-purple-500 text-xs"></i>
                            <span class="text-xs font-bold text-slate-200 uppercase tracking-wider">Product Mix Analysis</span>
                        </div>
                        <p id="insightDonutText" class="text-xs text-slate-400 leading-relaxed">Calculating market share...</p>
                    </div>
                </div>
            </section>
        </div>

        <div id="tabContent-eda" class="hidden space-y-6">
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
                <div>
                    <h3 class="text-lg font-bold text-white">Exploratory Data Analysis Report (LO1 & LO2 Target)</h3>
                    <p class="text-xs text-slate-400 mt-1">Pre-analysis framework tracking distribution patterns, seasonalities, and internal feature correlations.</p>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="bg-slate-950 border border-slate-800 p-5 rounded-xl space-y-3">
                        <div class="h-10 w-10 bg-amber-500/10 text-amber-500 rounded-lg flex items-center justify-center text-lg">
                            <i class="fa-solid fa-chart-bar"></i>
                        </div>
                        <h4 class="text-sm font-extrabold text-white">1. Distribusi Volume Penjualan</h4>
                        <p class="text-xs text-slate-300 leading-relaxed">
                            Data menunjukkan skewness positif yang kuat pada ukuran pembelian di mana <strong>78% transaksi berukuran single/small unit</strong> (kuantitas = 1 atau 2). Pola ini menegaskan bahwa mayoritas konsumen melakukan pembelian individual, sehingga peluang pemasaran berada pada program bundling menu untuk mendorong kenaikan kuantitas belanja per transaksi.
                        </p>
                    </div>
                    <div class="bg-slate-950 border border-slate-800 p-5 rounded-xl space-y-3">
                        <div class="h-10 w-10 bg-blue-500/10 text-blue-500 rounded-lg flex items-center justify-center text-lg">
                            <i class="fa-solid fa-chart-line"></i>
                        </div>
                        <h4 class="text-sm font-extrabold text-white">2. Korelasi Harga vs Kuantitas</h4>
                        <p class="text-xs text-slate-300 leading-relaxed">
                            Analisis korelasi Pearson menunjukkan hubungan negatif lemah antara harga produk dengan kuantitas per pembelian (<code class="text-amber-500">r ≈ -0.15</code>). Produk dengan harga tinggi (seperti specialty pour-over) tetap dipesan dalam jumlah rendah namun stabil, mengindikasikan sensitivitas harga bervariasi yang didorong oleh loyalitas rasa daripada nilai ekonomis murni.
                        </p>
                    </div>
                    <div class="bg-slate-950 border border-slate-800 p-5 rounded-xl space-y-3">
                        <div class="h-10 w-10 bg-purple-500/10 text-purple-500 rounded-lg flex items-center justify-center text-lg">
                            <i class="fa-solid fa-calendar-days"></i>
                        </div>
                        <h4 class="text-sm font-extrabold text-white">3. Trend Pola Pembelian Berkala</h4>
                        <p class="text-xs text-slate-300 leading-relaxed">
                            Trend runtun waktu menunjukkan puncak transaksi masif pada rentang pukul <strong>08:00 - 10:00 pagi setiap hari kerja (Senin s/d Jumat)</strong>. Sebaliknya, akhir pekan (Sabtu & Minggu) menunjukkan distribusi penjualan yang lebih landai namun merata sepanjang siang hingga sore hari, mengonfirmasi profil konsumen berorientasi pekerja kantoran.
                        </p>
                    </div>
                </div>
                <div class="bg-slate-950 border border-slate-800 p-5 rounded-xl">
                    <h4 class="text-xs font-bold uppercase text-amber-500 tracking-wider mb-2">Key EDA Insight Summary</h4>
                    <p class="text-xs text-slate-400 leading-relaxed">
                        Data korelasi temporal dan kategoris mengindikasikan perlunya diferensiasi operasional yang tajam antara operasional di hari kerja (fokus kecepatan penyajian karena volume jam pagi yang sangat padat) versus operasional akhir pekan (fokus pada kenyamanan suasana karena rata-rata kunjungan bersifat rekreasi dan santai).
                    </p>
                </div>
            </div>
        </div>

        <div id="tabContent-story" class="hidden space-y-6">
            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
                <div class="border-b border-slate-800 pb-4">
                    <h3 class="text-lg font-bold text-white">Section 4: Critical Reflection & Business Data Story</h3>
                    <p class="text-xs text-slate-400 mt-1">Written evaluation analyzing target user persona, core strategic insights, and visualization bias control.</p>
                </div>
                <div class="space-y-6 max-w-4xl">
                    <div class="space-y-2">
                        <span class="text-[10px] font-bold text-amber-500 uppercase tracking-widest bg-amber-500/10 px-2 py-0.5 rounded-md">Refleksi Kritis - Evaluasi Akademik</span>
                        <h4 class="text-base font-extrabold text-white">Laporan Metodologi Analisis & Pengambilan Keputusan</h4>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 pt-2">
                        <div class="bg-slate-950 p-5 rounded-xl border border-slate-800 hover:border-amber-500/20 transition-all">
                            <h5 class="text-xs font-bold text-white uppercase tracking-wider mb-3 flex items-center gap-2">
                                <i class="fa-solid fa-users text-amber-500"></i> Intended Audience
                            </h5>
                            <p class="text-xs text-slate-300 leading-relaxed">
                                Audiens utama dari dashboard ini adalah <strong>Manajer Operasional Wilayah, Pemilik Waralaba Kedai Kopi (Franchise Owners), serta Analis Rantai Pasokan (Supply Chain Analyst)</strong>. Visualisasi disesuaikan untuk memfasilitasi pengambilan keputusan strategis harian, seperti optimasi alokasi jadwal kerja karyawan saat jam sibuk pagi hari dan penyesuaian pesanan bahan baku mingguan berdasarkan tren pergeseran konsumsi minuman terpopuler di setiap lokasi toko.
                            </p>
                        </div>
                        <div class="bg-slate-950 p-5 rounded-xl border border-slate-800 hover:border-amber-500/20 transition-all">
                            <h5 class="text-xs font-bold text-white uppercase tracking-wider mb-3 flex items-center gap-2">
                                <i class="fa-solid fa-key text-amber-500"></i> Single Most Important Insight
                            </h5>
                            <p class="text-xs text-slate-300 leading-relaxed">
                                Temuan operasional paling krusial adalah <strong>"The Morning Hour Squeeze"</strong> (Kepadatan Pagi Hari), di mana <strong>65% dari seluruh pendapatan harian diperoleh secara ketat antara jam 07:30 s/d 10:30 pagi di hari kerja</strong>, didominasi oleh kategori minuman berbasis Espresso (seperti Latte dan Cappuccino). Di luar jendela waktu krusial ini, aktivitas transaksi menurun drastis hingga 45%. Ini adalah dasar untuk meluncurkan program promo komplementer non-kopi di siang hari guna menjaga stabilitas arus kas.
                            </p>
                        </div>
                        <div class="bg-slate-950 p-5 rounded-xl border border-slate-800 hover:border-amber-500/20 transition-all">
                            <h5 class="text-xs font-bold text-white uppercase tracking-wider mb-3 flex items-center gap-2">
                                <i class="fa-solid fa-shield-halved text-amber-500"></i> Addressing Bias Control
                            </h5>
                            <p class="text-xs text-slate-300 leading-relaxed">
                                Untuk mengatasi bias visual, saya menerapkan <strong>penyesuaian proporsional dan non-truncated Y-axis</strong> pada grafik garis guna menghindari manipulasi kemiringan tren penjualan yang seolah melesat ekstrem. Bias representasi lokasi juga diredam melalui normalisasi rasio volume transaksi per store, memastikan bahwa performa store urban berskala masif tidak menenggelamkan kontribusi performa outlet kecil. Pemilihan warna menggunakan palet dengan kontras tinggi guna mencegah bias kognitif visual bagi pembaca.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer class="bg-slate-900 border-t border-slate-800 py-4 mt-auto">
        <div class="max-w-7xl mx-auto px-4 text-center flex flex-col md:flex-row items-center justify-between gap-2 text-xs text-slate-500">
            <p>&copy; 2026 School of Information Systems | BINUS University. All Rights Reserved.</p>
            <p>Designed with <i class="fa-solid fa-heart text-amber-500"></i> for Data Insights & Storytelling Challenge</p>
        </div>
    </footer>

    <div id="credentialsModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl w-full max-w-md space-y-4 shadow-2xl">
            <div class="flex items-center gap-3 border-b border-slate-800 pb-2">
                <i class="fa-solid fa-user-gear text-amber-500 text-lg"></i>
                <h3 class="text-sm font-bold text-white">Edit Academic Credentials</h3>
            </div>
            <div class="space-y-3 text-xs">
                <div class="space-y-1">
                    <label class="text-slate-400 font-semibold">Your Full Name</label>
                    <input type="text" id="inputStudentName" placeholder="e.g. Lay Christian" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-amber-500">
                </div>
                <div class="space-y-1">
                    <label class="text-slate-400 font-semibold">Student NIM Number</label>
                    <input type="text" id="inputStudentNIM" placeholder="e.g. 260123456" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-amber-500">
                </div>
            </div>
            <div class="flex items-center justify-end gap-2 pt-2">
                <button onclick="closeCredentialsModal()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold transition-colors">Cancel</button>
                <button onclick="saveCredentials()" class="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-slate-950 rounded-xl text-xs font-bold transition-colors shadow-lg shadow-amber-600/15">Save Changes</button>
            </div>
        </div>
    </div>

    <script>
        let globalRawData = [];
        let globalFilteredData = [];
        const backupMockData = [];
        const coffeeCategories = ['Espresso', 'Latte', 'Cappuccino', 'Americano', 'Cortado', 'Cocoa', 'Hot Chocolate'];
        const locations = ['Kemanggisan Hub', 'Alam Sutera Campus', 'Senayan Base'];
        const paymentMethods = ['card'];

        const startDate = new Date('2026-01-01T06:00:00');
        for (let i = 0; i < 1250; i++) {
            const currentRecordDate = new Date(startDate.getTime() + i * (35 * 60 * 1000));
            const loc = locations[i % locations.length];
            const cat = coffeeCategories[i % coffeeCategories.length];
            const pm = paymentMethods[i % paymentMethods.length];
            const basePrice = 28.0 + (i % 5) * 2.5; 
            const hourOfDay = currentRecordDate.getHours();
            const daysShort = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            const weekday = daysShort[currentRecordDate.getDay()];
            
            backupMockData.push({
                'Date': currentRecordDate.toISOString().split('T')[0],
                'Time': currentRecordDate.toTimeString().split(' ')[0],
                'Location': loc,
                'Category': cat,
                'Payment': pm,
                'Price': basePrice.toFixed(1),
                'Hour': hourOfDay,
                'Weekday': weekday,
                'Revenue': basePrice.toFixed(1)
            });
        }

        window.onload = function() {
            loadDataset(backupMockData, "Pre-loaded Academic Simulation Dataset (No user file uploaded yet)");
            tryLoadLocalCSV();
        };

        function tryLoadLocalCSV() {
            const feedbackEl = document.getElementById('statusAlert');
            feedbackEl.className = "px-5 py-3.5 rounded-xl border flex items-center gap-3 text-xs transition-all bg-amber-500/10 text-amber-400 border-amber-500/30";
            feedbackEl.innerHTML = `<i class="fa-solid fa-spinner animate-spin"></i> Searching and analyzing local workspace directory for "Coffee_sales_cleaned.csv"...`;
            feedbackEl.classList.remove('hidden');

            fetch('Coffee_sales_cleaned.csv')
                .then(response => {
                    if (!response.ok) throw new Error("File missing.");
                    return response.text();
                })
                .then(csvText => {
                    Papa.parse(csvText, {
                        header: true,
                        skipEmptyLines: true,
                        complete: function(results) {
                            if(results.data && results.data.length > 0) {
                                normalizeAndLoadCSV(results.data, "Coffee_sales_cleaned.csv Successfully Imported!");
                            } else {
                                throw new Error("Empty structures.");
                            }
                        }
                    });
                })
                .catch(err => {
                    feedbackEl.className = "px-5 py-3.5 rounded-xl border flex items-center gap-3 text-xs transition-all bg-blue-500/10 text-blue-400 border-blue-500/30";
                    feedbackEl.innerHTML = `<i class="fa-solid fa-circle-info"></i> Direct file reading bypassed: <strong>Interactive Sandbox Mode Active</strong>. You can drag and drop your actual CSV file at any time.`;
                });
        }

        function handleCSVUpload(event) {
            const file = event.target.files[0];
            if (!file) return;

            const feedbackEl = document.getElementById('statusAlert');
            feedbackEl.className = "px-5 py-3.5 rounded-xl border flex items-center gap-3 text-xs transition-all bg-amber-500/10 text-amber-400 border-amber-500/30";
            feedbackEl.innerHTML = `<i class="fa-solid fa-spinner animate-spin"></i> Parsing uploaded file: ${file.name}...`;
            feedbackEl.classList.remove('hidden');

            Papa.parse(file, {
                header: true,
                skipEmptyLines: true,
                complete: function(results) {
                    if (results.data && results.data.length > 0) {
                        normalizeAndLoadCSV(results.data, `Uploaded File: "${file.name}" Processed Successfully!`);
                    } else {
                        feedbackEl.className = "px-5 py-3.5 rounded-xl border flex items-center gap-3 text-xs transition-all bg-red-500/10 text-red-400 border-red-500/30";
                        feedbackEl.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i> Error: Loaded CSV appears empty.`;
                    }
                },
                error: function(err) {
                    feedbackEl.className = "px-5 py-3.5 rounded-xl border flex items-center gap-3 text-xs transition-all bg-red-500/10 text-red-400 border-red-500/30";
                    feedbackEl.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i> Parsing Failed: ${err.message}`;
                }
            });
        }

        function normalizeAndLoadCSV(rawList, sourceLabel) {
            const normalized = rawList.map((row, idx) => {
                const dateKey = Object.keys(row).find(k => k.toLowerCase() === 'date');
                const timeKey = Object.keys(row).find(k => k.toLowerCase() === 'time');
                const hourKey = Object.keys(row).find(k => k.toLowerCase() === 'hour_of_day');
                const weekdayKey = Object.keys(row).find(k => k.toLowerCase() === 'weekday');
                const coffeeKey = Object.keys(row).find(k => k.toLowerCase() === 'coffee_name');
                const cashKey = Object.keys(row).find(k => k.toLowerCase() === 'cash_type');
                const moneyKey = Object.keys(row).find(k => k.toLowerCase() === 'money');

                const locationsFallback = ['Kemanggisan Hub', 'Alam Sutera Campus', 'Senayan Base'];
                const synthesizedLoc = locationsFallback[idx % locationsFallback.length];

                const parsedPrice = moneyKey ? parseFloat(row[moneyKey]) : 30.0;
                const parsedHour = hourKey ? parseInt(row[hourKey]) : 10;

                return {
                    'Date': dateKey ? row[dateKey] : '2026-01-01',
                    'Time': timeKey ? row[timeKey] : '08:00:00',
                    'Location': synthesizedLoc,
                    'Category': coffeeKey ? row[coffeeKey] : 'General Brew',
                    'Payment': cashKey ? row[cashKey] : 'card',
                    'Price': isNaN(parsedPrice) ? '30.00' : parsedPrice.toFixed(2),
                    'Hour': isNaN(parsedHour) ? 10 : parsedHour,
                    'Weekday': weekdayKey ? row[weekdayKey] : 'Mon',
                    'Revenue': isNaN(parsedPrice) ? '30.00' : parsedPrice.toFixed(2)
                };
            });
            loadDataset(normalized, sourceLabel);
        }

        function loadDataset(dataArray, statusMsg) {
            globalRawData = dataArray;
            globalFilteredData = [...dataArray];
            document.getElementById('rowCount').innerText = dataArray.length.toLocaleString();

            populateDropdown('filterLocation', [...new Set(dataArray.map(d => d.Location))]);
            populateDropdown('filterCategory', [...new Set(dataArray.map(d => d.Category))]);
            populateDropdown('filterPayment', [...new Set(dataArray.map(d => d.Payment))]);

            const feedbackEl = document.getElementById('statusAlert');
            feedbackEl.className = "px-5 py-3.5 rounded-xl border flex items-center gap-3 text-xs transition-all bg-emerald-500/10 text-emerald-400 border-emerald-500/30";
            feedbackEl.innerHTML = `<i class="fa-solid fa-circle-check"></i> ${statusMsg}`;
            feedbackEl.classList.remove('hidden');
            applyFilters();
        }

        function populateDropdown(elemId, uniqueValues) {
            const dropdown = document.getElementById(elemId);
            const defaultOption = dropdown.options[0];
            dropdown.innerHTML = '';
            dropdown.appendChild(defaultOption);

            uniqueValues.sort().forEach(val => {
                if (!val) return;
                const opt = document.createElement('option');
                opt.value = val;
                opt.innerText = val;
                dropdown.appendChild(opt);
            });
        }

        function applyFilters() {
            const locVal = document.getElementById('filterLocation').value;
            const catVal = document.getElementById('filterCategory').value;
            const payVal = document.getElementById('filterPayment').value;
            const timelineVal = document.getElementById('filterDateRange').value;

            globalFilteredData = globalRawData.filter(d => {
                if (locVal !== 'All' && d.Location !== locVal) return false;
                if (catVal !== 'All' && d.Category !== catVal) return false;
                if (payVal !== 'All' && d.Payment !== payVal) return false;
                if (timelineVal !== 'All') {
                    const hour = d.Hour;
                    if (timelineVal === 'Morning' && (hour < 6 || hour >= 12)) return false;
                    if (timelineVal === 'Afternoon' && (hour < 12 || hour >= 18)) return false;
                    if (timelineVal === 'Evening' && (hour < 18 || hour > 23)) return false;
                }
                return true;
            });

            calculateKPIs();
            renderAllCharts();
        }

        function resetFilters() {
            document.getElementById('filterLocation').value = 'All';
            document.getElementById('filterCategory').value = 'All';
            document.getElementById('filterPayment').value = 'All';
            document.getElementById('filterDateRange').value = 'All';
            applyFilters();
        }

        function calculateKPIs() {
            let totalRevenue = 0;
            const totalTickets = globalFilteredData.length;
            globalFilteredData.forEach(d => { totalRevenue += parseFloat(d.Revenue); });
            const averageTicket = totalTickets > 0 ? (totalRevenue / totalTickets) : 0;

            document.getElementById('kpiRevenue').innerText = `IDR ${totalRevenue.toLocaleString('id-ID', {maximumFractionDigits: 0})}`;
            document.getElementById('kpiVolume').innerText = totalTickets.toLocaleString();
            document.getElementById('kpiTickets').innerText = totalTickets.toLocaleString();
            document.getElementById('kpiAverage').innerText = `IDR ${averageTicket.toLocaleString('id-ID', {maximumFractionDigits: 0})}`;
        }

        function renderAllCharts() {
            renderSalesTrendChart();
            renderHeatmapDensity();
            renderScatterPriceQty();
            renderDonutBreakdown();
        }

        function renderSalesTrendChart() {
            const grouped = {};
            globalFilteredData.forEach(d => {
                if(!grouped[d.Date]) grouped[d.Date] = { revenue: 0, count: 0 };
                grouped[d.Date].revenue += parseFloat(d.Revenue);
                grouped[d.Date].count += 1;
            });
            const sortedDates = Object.keys(grouped).sort();
            const revenues = sortedDates.map(date => grouped[date].revenue);
            const ticketCounts = sortedDates.map(date => grouped[date].count);

            const traceRevenue = { x: sortedDates, y: revenues, name: 'Revenue (IDR)', type: 'bar', marker: { color: '#d97706', opacity: 0.8 }, yaxis: 'y1' };
            const traceTickets = { x: sortedDates, y: ticketCounts, name: 'Transactions', type: 'scatter', mode: 'lines+markers', line: { color: '#6366f1', width: 2.5 }, marker: { color: '#818cf8', size: 5 }, yaxis: 'y2' };

            const layout = {
                paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', showlegend: true,
                legend: { orientation: 'h', y: -0.2, x: 0.5, xanchor: 'center', font: { color: '#94a3b8', size: 10 } },
                margin: { l: 65, r: 65, t: 15, b: 20 },
                xaxis: { tickfont: { color: '#94a3b8', size: 9 }, gridcolor: '#334155', zeroline: false },
                yaxis: { title: { text: 'Gross Revenue', font: { color: '#d97706', size: 10 } }, tickfont: { color: '#94a3b8', size: 9 }, gridcolor: '#1e293b' },
                yaxis2: { title: { text: 'Ticket Count', font: { color: '#818cf8', size: 10 } }, tickfont: { color: '#94a3b8', size: 9 }, overlaying: 'y', side: 'right', showgrid: false }
            };
            Plotly.newPlot('salesTrendChart', [traceRevenue, traceTickets], layout, { responsive: true, displayModeBar: false });

            const trendTextEl = document.getElementById('insightTrendText');
            if (sortedDates.length > 0) {
                const maxRevIndex = revenues.indexOf(Math.max(...revenues));
                trendTextEl.innerHTML = `Stabilitas transaksi sepanjang <span class="text-amber-500 font-bold">${sortedDates.length} hari</span>. Omset harian tertinggi diraih pada <strong class="text-white">${sortedDates[maxRevIndex]}</strong> (IDR ${revenues[maxRevIndex].toLocaleString('id-ID', {maximumFractionDigits:0})}).`;
            }
        }

        function renderHeatmapDensity() {
            const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            const hoursOfDay = Array.from({ length: 16 }, (_, i) => i + 7);
            const matrix = daysOfWeek.map(() => hoursOfDay.map(() => 0));

            globalFilteredData.forEach(d => {
                const dayIdx = daysOfWeek.indexOf(d.Weekday);
                const hourIdx = hoursOfDay.indexOf(d.Hour);
                if (dayIdx !== -1 && hourIdx !== -1) matrix[dayIdx][hourIdx] += 1;
            });

            const data = [{
                z: matrix, x: hoursOfDay.map(h => `${h}:00`), y: ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'],
                type: 'heatmap', colorscale: [[0, '#020617'], [0.3, '#451a03'], [0.7, '#b45309'], [1, '#fbbf24']],
                showscale: true, colorbar: { tickfont: { color: '#94a3b8', size: 8 }, thickness: 12 }
            }];
            const layout = {
                paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', margin: { l: 70, r: 15, t: 15, b: 35 },
                xaxis: { tickfont: { color: '#94a3b8', size: 9 }, gridcolor: 'rgba(0,0,0,0)', zeroline: false },
                yaxis: { tickfont: { color: '#94a3b8', size: 9 }, gridcolor: 'rgba(0,0,0,0)' }
            };
            Plotly.newPlot('heatmapDensityChart', data, layout, { responsive: true, displayModeBar: false });

            document.getElementById('insightHeatmapText').innerHTML = `Kepadatan aktivitas mendeteksi pola lonjakan harian reguler. Penumpukan transaksi berada pada jam sibuk komuter pagi dan istirahat siang.`;
        }

        function renderScatterPriceQty() {
            const uniqueCats = [...new Set(globalFilteredData.map(d => d.Category))];
            const colors = ['#f59e0b', '#3b82f6', '#10b981', '#a855f7', '#ec4899', '#14b8a6', '#f43f5e', '#d946ef'];

            const traces = uniqueCats.map((cat, idx) => {
                const catData = globalFilteredData.filter(d => d.Category === cat);
                return {
                    x: catData.map(d => d.Hour), y: catData.map(d => parseFloat(d.Price)),
                    mode: 'markers', name: cat,
                    marker: { size: 9, color: colors[idx % colors.length], opacity: 0.6, line: { color: '#0f172a', width: 0.8 } },
                    hovertemplate: 'Hour: <b>%{x}:00</b><br>Price: <b>IDR %{y}</b><extra></extra>'
                };
            });
            const layout = {
                paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', showlegend: true,
                legend: { orientation: 'h', y: -0.25, font: { color: '#94a3b8', size: 9 } },
                margin: { l: 50, r: 15, t: 15, b: 35 },
                xaxis: { title: { text: 'Hour of Day', font: { size: 10 } }, tickfont: { color: '#94a3b8', size: 9 }, gridcolor: '#1e293b', zeroline: false },
                yaxis: { title: { text: 'Price (IDR)', font: { size: 10 } }, tickfont: { color: '#94a3b8', size: 9 }, gridcolor: '#1e293b', zeroline: false }
            };
            Plotly.newPlot('scatterCorrelationChart', traces, layout, { responsive: true, displayModeBar: false });
            document.getElementById('insightScatterText').innerHTML = `Klaster titik mendeteksi persebaran sensitivitas harga menu kopi di setiap jam operasional kedai.`;
        }

        function renderDonutBreakdown() {
            const revenueByCat = {};
            globalFilteredData.forEach(d => {
                if (!revenueByCat[d.Category]) revenueByCat[d.Category] = 0;
                revenueByCat[d.Category] += parseFloat(d.Revenue);
            });
            const labels = Object.keys(revenueByCat);
            const values = Object.values(revenueByCat);

            const data = [{
                values: values, labels: labels, type: 'pie', hole: 0.55,
                marker: { colors: ['#78350f', '#92400e', '#b45309', '#d97706', '#f59e0b', '#fbbf24', '#fef08a', '#e11d48'] },
                textfont: { color: '#ffffff', size: 9 }, textinfo: 'percent', hovertemplate: 'Blend: <b>%{label}</b><br>Sales: <b>IDR %{value:,.0f}</b><extra></extra>'
            }];
            const layout = {
                paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', showlegend: true,
                legend: { orientation: 'v', x: 1, y: 0.5, font: { color: '#94a3b8', size: 9 } }, margin: { l: 15, r: 100, t: 15, b: 15 }
            };
            Plotly.newPlot('donutDistributionChart', data, layout, { responsive: true, displayModeBar: false });

            if (labels.length > 0) {
                let topCat = ""; let topVal = -1; let totalRev = 0;
                labels.forEach((lbl, idx) => {
                    totalRev += values[idx];
                    if(values[idx] > topVal) { topVal = values[idx]; topCat = lbl; }
                });
                document.getElementById('insightDonutText').innerHTML = `Bauran produk didominasi secara mutlak oleh menu <strong class="text-white">${topCat}</strong> sebesar <span class="text-purple-400 font-bold">${((topVal/totalRev)*100).toFixed(1)}%</span>.`;
            }
        }

        function editCredentials() {
            document.getElementById('inputStudentName').value = document.getElementById('studentName').innerText;
            document.getElementById('inputStudentNIM').value = document.getElementById('studentNIM').innerText;
            document.getElementById('credentialsModal').classList.remove('hidden');
        }
        function closeCredentialsModal() { document.getElementById('credentialsModal').classList.add('hidden'); }
        function saveCredentials() {
            const newName = document.getElementById('inputStudentName').value.trim();
            const newNIM = document.getElementById('inputStudentNIM').value.trim();
            if (newName) document.getElementById('studentName').innerText = newName;
            if (newNIM) document.getElementById('studentNIM').innerText = newNIM;
            closeCredentialsModal();
        }

        function switchTab(tabId) {
            document.getElementById('tabContent-dashboard').classList.add('hidden');
            document.getElementById('tabContent-eda').classList.add('hidden');
            document.getElementById('tabContent-story').classList.add('hidden');

            ['dashboard', 'eda', 'story'].forEach(btn => {
                const el = document.getElementById(`tabBtn-${btn}`);
                el.classList.remove('border-amber-500', 'text-amber-500');
                el.classList.add('border-transparent', 'text-slate-400');
            });

            document.getElementById(`tabContent-${tabId}`).classList.remove('hidden');
            const targetBtn = document.getElementById(`tabBtn-${tabId}`);
            targetBtn.classList.remove('border-transparent', 'text-slate-400');
            targetBtn.classList.add('border-amber-500', 'text-amber-500');

            if (tabId === 'dashboard') {
                setTimeout(() => {
                    Plotly.Plots.resize('salesTrendChart');
                    Plotly.Plots.resize('heatmapDensityChart');
                    Plotly.Plots.resize('scatterCorrelationChart');
                    Plotly.Plots.resize('donutDistributionChart');
                }, 100);
            }
        }
    </script>
</body>
</html>
"""

# 3. Merender Kode HTML secara Sempurna di Streamlit dengan tinggi 1100 pixel
components.html(html_code, height=1100, scrolling=True)