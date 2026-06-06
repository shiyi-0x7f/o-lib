import { useState, useEffect, useCallback, useMemo } from "react";
import { invoke } from "@tauri-apps/api/core";
import { confirm } from "@tauri-apps/plugin-dialog";
import {
    FileText, Folder, Trash2, ExternalLink,
    FolderOpen, RefreshCw, Wifi, WifiOff,
    BookOpen, Image, Film, Package,
} from "lucide-react";
import ContextMenu, { ContextMenuItem } from "../components/ContextMenu";
import WirelessTransfer from "../components/WirelessTransfer";

interface FileInfo {
    name: string;
    path: string;
    is_dir: boolean;
    size: number;
    extension: string;
    modified?: string;
}

function formatSize(bytes: number): string {
    if (!bytes) return "—";
    const units = ["B", "KB", "MB", "GB"];
    let i = 0;
    let size = bytes;
    while (size >= 1024 && i < units.length - 1) {
        size /= 1024;
        i++;
    }
    return `${size.toFixed(1)} ${units[i]}`;
}

function getFileIconClass(ext: string): string {
    switch (ext.toLowerCase()) {
        case "pdf": return "pdf";
        case "epub": return "epub";
        case "mobi":
        case "azw3": return "mobi";
        default: return "default";
    }
}

export default function BookshelfPage() {
    const [files, setFiles] = useState<FileInfo[]>([]);
    const [loading, setLoading] = useState(false);
    const [activeFilter, setActiveFilter] = useState<string>("全部");
    const [activeSubFilter, setActiveSubFilter] = useState<string | null>(null);
    const [contextMenu, setContextMenu] = useState<{ x: number; y: number; file: FileInfo } | null>(null);
    const [showWireless, setShowWireless] = useState(false);
    const [lanRunning, setLanRunning] = useState(false);

    // Poll LAN server status
    useEffect(() => {
        const checkStatus = async () => {
            try {
                const s: { running: boolean } = await invoke("get_lan_status");
                setLanRunning(s.running);
            } catch { /* ignore */ }
        };
        checkStatus();
        const interval = setInterval(checkStatus, 3000);
        return () => clearInterval(interval);
    }, []);

    // Category definitions for grouping file types
    const CATEGORIES: Record<string, { exts: Set<string>; icon: string }> = useMemo(() => ({
        "电子书": { exts: new Set(["PDF", "EPUB", "MOBI", "AZW3", "AZW", "FB2", "DJVU", "CBZ", "CBR"]), icon: "book" },
        "文档":   { exts: new Set(["DOC", "DOCX", "PPT", "PPTX", "XLS", "XLSX", "CSV", "TXT", "MD", "RTF", "ODT", "ODS", "ODP"]), icon: "doc" },
        "图片":   { exts: new Set(["JPG", "JPEG", "PNG", "GIF", "BMP", "SVG", "WEBP", "AVIF", "TIFF", "TIF", "ICO", "PSD", "EPS"]), icon: "image" },
        "音视频": { exts: new Set(["MP4", "MP3", "AVI", "MKV", "MOV", "WAV", "FLAC", "AAC", "OGG", "WMV", "WEBM", "M4A", "M4V"]), icon: "media" },
    }), []);

    // Compute category-based filter options with counts
    const filterOptions = useMemo(() => {
        const categoryCounts: Record<string, number> = {};
        let folderCount = 0;
        let otherCount = 0;

        for (const f of files) {
            if (f.is_dir) {
                folderCount++;
                continue;
            }
            if (!f.extension) { otherCount++; continue; }
            const ext = f.extension.toUpperCase();
            let matched = false;
            for (const [cat, { exts }] of Object.entries(CATEGORIES)) {
                if (exts.has(ext)) {
                    categoryCounts[cat] = (categoryCounts[cat] || 0) + 1;
                    matched = true;
                    break;
                }
            }
            if (!matched) otherCount++;
        }

        const opts: { label: string; count: number }[] = [
            { label: "全部", count: files.length },
        ];
        if (folderCount > 0) opts.push({ label: "文件夹", count: folderCount });
        for (const cat of Object.keys(CATEGORIES)) {
            if (categoryCounts[cat]) opts.push({ label: cat, count: categoryCounts[cat] });
        }
        if (otherCount > 0) opts.push({ label: "其他", count: otherCount });
        return opts;
    }, [files, CATEGORIES]);

    // Reset filter if the active option no longer exists
    useEffect(() => {
        if (activeFilter !== "全部" && !filterOptions.some(o => o.label === activeFilter)) {
            setActiveFilter("全部");
            setActiveSubFilter(null);
        }
    }, [filterOptions, activeFilter]);

    // Clear sub-filter when switching categories
    const handleCategoryClick = useCallback((label: string) => {
        if (activeFilter === label) {
            // Clicking same category again: reset to "全部"
            setActiveFilter("全部");
            setActiveSubFilter(null);
        } else {
            setActiveFilter(label);
            setActiveSubFilter(null);
        }
    }, [activeFilter]);

    // Compute sub-options for the active category
    const subFilterOptions = useMemo(() => {
        // Only show sub-filters for actual categories (not 全部/文件夹)
        const cat = CATEGORIES[activeFilter];
        if (!cat) return null;

        const counts: Record<string, number> = {};
        for (const f of files) {
            if (f.is_dir || !f.extension) continue;
            const ext = f.extension.toUpperCase();
            if (cat.exts.has(ext)) {
                counts[ext] = (counts[ext] || 0) + 1;
            }
        }
        const exts = Object.entries(counts).sort((a, b) => b[1] - a[1]);
        // Only show sub-filters if there are 2+ different formats
        if (exts.length < 2) return null;
        return exts.map(([ext, count]) => ({ label: ext, count }));
    }, [files, activeFilter, CATEGORIES]);

    // Also compute sub-options for "其他" category
    const otherSubFilterOptions = useMemo(() => {
        if (activeFilter !== "其他") return null;
        const counts: Record<string, number> = {};
        for (const f of files) {
            if (f.is_dir || !f.extension) continue;
            const ext = f.extension.toUpperCase();
            if (!Object.values(CATEGORIES).some(({ exts }) => exts.has(ext))) {
                counts[ext] = (counts[ext] || 0) + 1;
            }
        }
        const exts = Object.entries(counts).sort((a, b) => b[1] - a[1]);
        if (exts.length < 2) return null;
        return exts.map(([ext, count]) => ({ label: ext, count }));
    }, [files, activeFilter, CATEGORIES]);

    const activeSubOptions = subFilterOptions || otherSubFilterOptions;

    // Filtered file list based on category + sub-filter
    const filteredFiles = useMemo(() => {
        if (activeFilter === "全部") return files;
        if (activeFilter === "文件夹") return files.filter(f => f.is_dir);

        // If a specific sub-format is selected, filter to just that extension
        if (activeSubFilter) {
            return files.filter(f => !f.is_dir && f.extension?.toUpperCase() === activeSubFilter);
        }

        if (activeFilter === "其他") {
            return files.filter(f => {
                if (f.is_dir) return false;
                if (!f.extension) return true;
                const ext = f.extension.toUpperCase();
                return !Object.values(CATEGORIES).some(({ exts }) => exts.has(ext));
            });
        }
        const cat = CATEGORIES[activeFilter];
        if (!cat) return files;
        return files.filter(f => !f.is_dir && cat.exts.has(f.extension?.toUpperCase() || ""));
    }, [files, activeFilter, activeSubFilter, CATEGORIES]);

    const loadFiles = async () => {
        setLoading(true);
        try {
            const result: FileInfo[] = await invoke("list_files", { dir: null });
            setFiles(result);
        } catch (err) {
            console.error("Failed to load files:", err);
        }
        setLoading(false);
    };

    useEffect(() => {
        loadFiles();
    }, []);

    const handleOpen = async (file: FileInfo) => {
        try {
            await invoke("open_file", { path: file.path });
        } catch (err) {
            console.error("Failed to open file:", err);
        }
    };

    const handleDelete = async (file: FileInfo) => {
        const confirmed = await confirm(`确定要删除 "${file.name}" 吗？`, {
            title: "删除确认",
            kind: "warning",
            okLabel: "删除",
            cancelLabel: "取消",
        });
        if (!confirmed) return;
        try {
            await invoke("delete_file", { path: file.path });
            await loadFiles();
        } catch (err) {
            console.error("Failed to delete:", err);
        }
    };

    const handleOpenInExplorer = async (file: FileInfo) => {
        try {
            await invoke("open_in_explorer", { path: file.path });
        } catch (err) {
            console.error("Failed to open in explorer:", err);
        }
    };

    const handleContextMenu = useCallback((e: React.MouseEvent, file: FileInfo) => {
        e.preventDefault();
        e.stopPropagation();
        setContextMenu({ x: e.clientX, y: e.clientY, file });
    }, []);

    const closeContextMenu = useCallback(() => {
        setContextMenu(null);
    }, []);

    const getContextMenuItems = (file: FileInfo): ContextMenuItem[] => {
        const items: ContextMenuItem[] = [
            {
                label: '打开文件',
                icon: <ExternalLink size={15} />,
                onClick: () => handleOpen(file),
            },
            {
                label: '在文件夹中打开',
                icon: <FolderOpen size={15} />,
                onClick: () => handleOpenInExplorer(file),
            },
            { label: '', onClick: () => { }, divider: true },
            {
                label: '删除',
                icon: <Trash2 size={15} />,
                onClick: () => handleDelete(file),
                danger: true,
            },
        ];
        return items;
    };

    return (
        <div className="page-container">
            <div className="page-header flex items-center justify-between">
                <div>
                    <h1 className="page-title">书架</h1>
                    <p className="page-subtitle">管理已下载的电子书</p>
                </div>
                <div className="flex gap-2">
                    <button
                        className={`btn btn-sm ${lanRunning ? "btn-wireless-active" : "btn-secondary"}`}
                        onClick={() => setShowWireless(true)}
                    >
                        {lanRunning ? (
                            <>
                                <span className="wireless-dot" />
                                <Wifi size={14} />
                                传书中
                            </>
                        ) : (
                            <>
                                <WifiOff size={14} />
                                无线传书
                            </>
                        )}
                    </button>
                    <button className="btn btn-secondary btn-sm" onClick={loadFiles}>
                        <RefreshCw size={14} />
                        刷新
                    </button>
                </div>
            </div>

            {/* Inline filter chips */}
            {files.length > 0 && filterOptions.length > 1 && (
                <div className="filter-chips-wrapper">
                    <div className="filter-chips">
                        {filterOptions.map(opt => (
                            <button
                                key={opt.label}
                                className={`filter-chip ${activeFilter === opt.label ? "filter-chip-active" : ""}`}
                                onClick={() => handleCategoryClick(opt.label)}
                            >
                                {opt.label === "文件夹" && <Folder size={13} />}
                                {opt.label === "电子书" && <BookOpen size={13} />}
                                {opt.label === "文档" && <FileText size={13} />}
                                {opt.label === "图片" && <Image size={13} />}
                                {opt.label === "音视频" && <Film size={13} />}
                                {opt.label === "其他" && <Package size={13} />}
                                <span>{opt.label}</span>
                                <span className="filter-chip-count">{opt.count}</span>
                            </button>
                        ))}
                    </div>
                    {/* Secondary sub-filter row */}
                    {activeSubOptions && (
                        <div className="filter-sub-chips">
                            <button
                                className={`filter-sub-chip ${activeSubFilter === null ? "filter-sub-chip-active" : ""}`}
                                onClick={() => setActiveSubFilter(null)}
                            >
                                全部
                            </button>
                            {activeSubOptions.map(sub => (
                                <button
                                    key={sub.label}
                                    className={`filter-sub-chip ${activeSubFilter === sub.label ? "filter-sub-chip-active" : ""}`}
                                    onClick={() => setActiveSubFilter(sub.label)}
                                >
                                    {sub.label}
                                    <span className="filter-sub-chip-count">{sub.count}</span>
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            )}

            <div style={{
                height: "calc(100vh - 180px)",
                overflow: "hidden",
                display: "flex",
                flexDirection: "column"
            }}>
                <div className="card" style={{
                    padding: 8,
                    flex: 1,
                    overflow: "auto",
                    minHeight: 0
                }}>
                    {loading ? (
                        <div className="empty-state" style={{ padding: 40 }}>
                            <RefreshCw size={24} className="spinner" />
                        </div>
                    ) : files.length === 0 ? (
                        <div className="empty-state" style={{ padding: 40 }}>
                            <FolderOpen size={36} className="empty-state-icon" />
                            <p className="empty-state-text">下载文件夹为空</p>
                            <p className="empty-state-hint">搜索并下载书籍后将显示在此处</p>
                        </div>
                    ) : (
                        filteredFiles.map((file) => (
                            <div
                                key={file.path}
                                className="file-item"
                                onDoubleClick={() => handleOpen(file)}
                                onContextMenu={(e) => handleContextMenu(e, file)}
                            >
                                <div className={`file-icon ${file.is_dir ? "" : getFileIconClass(file.extension)}`}>
                                    {file.is_dir ? (
                                        <Folder size={20} />
                                    ) : (
                                        <FileText size={20} />
                                    )}
                                </div>
                                <div className="file-info">
                                    <div className="file-name">{file.name}</div>
                                    <div className="file-meta">
                                        {file.is_dir ? "文件夹" : formatSize(file.size)}
                                        {file.modified && ` · ${file.modified}`}
                                    </div>
                                </div>
                                {!file.is_dir && (
                                    <span className="badge badge-accent">
                                        {file.extension.toUpperCase()}
                                    </span>
                                )}
                            </div>
                        ))
                    )}
                </div>
            </div>
            {/* Context Menu */}
            {contextMenu && (
                <ContextMenu
                    x={contextMenu.x}
                    y={contextMenu.y}
                    items={getContextMenuItems(contextMenu.file)}
                    onClose={closeContextMenu}
                />
            )}
            {/* Wireless Transfer Dialog */}
            {showWireless && (
                <WirelessTransfer onClose={() => setShowWireless(false)} />
            )}
        </div>
    );
}
