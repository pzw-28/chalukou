$input = 'C:\Users\27189\Desktop\chalukou\deliverables\岔路口_预指导介绍.docx'
$output = 'C:\Users\27189\Desktop\chalukou\deliverables\岔路口_预指导介绍.pdf'
$word = New-Object -ComObject Kwps.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
  Write-Output 'Opening DOCX'
  $document = $word.Documents.Open($input, $false, $true)
  Write-Output 'Exporting PDF'
  $document.ExportAsFixedFormat($output, 17)
  $document.Close()
  Write-Output "Exported $output"
} finally {
  $word.Quit()
}
