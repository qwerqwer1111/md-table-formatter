# md-table-formatter

Markdown のテーブルを整形します.

## Sample

入力

```markdown
|Left align|Center align|Right align|
|:-|:-:|-:|
|Content|Content|Content|
|Content|Content|Content|
```

出力

```markdown
| Left align | Center align | Right align |
|:-----------|:------------:|------------:|
| Content    |   Content    |     Content |
| Content    |   Content    |     Content |
```

## Usage

Emacs から利用する場合, `~/.emacs.d/init.el`に下記のように記載すれば, `C-x t`で選択範囲内のテーブルを整形できます.

```elisp
(defun md-table-formatter (start end)
 (interactive "r")
 (save-excursion
   (shell-command-on-region start end "python /path/to/md-table-formatter.py" nil t)))
(global-set-key (kbd "C-x t") 'md-table-formatter)
```
