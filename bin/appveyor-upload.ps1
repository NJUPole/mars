If ($env:APPVEYOR_REPO_TAG -eq "true"){
    Invoke-Expression "python setup.py bdist_wheel"
    Invoke-Expression "twine upload --skip-existing dist/* --verbose"
}Else {
    write-output "Not on a tag commit, won't deploy to pypi"
}