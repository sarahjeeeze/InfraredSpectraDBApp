file = open("game.txt", "r")

#splitfile

splitfile = file.read().split()

#get rid of ' and , and print required code
for tableName in splitfile:
    corrected = tableName.replace("`","")
    corrected = corrected.replace(",","")
    print('setup_schema(None,' + corrected + ')')
    print(corrected + 'schema =' + corrected + '.__colanderalchemy__' + ',')
    #print(corrected + 'schema = deform.Form(schema, buttons=(' +'\'submit\''+',))')

#create dictionaryfor retrun

output = {}
# do the same for form.render() and create return dictionary


for tableName in splitfile:
    corrected1 = tableName.replace("`","")
    corrected = corrected1.replace(",","") + 'schema'
    form = corrected1.replace(",","") + 'form'
    print(form +'='+ corrected+'.render()')
    
    output[form] = (form)
#print return output
print(output)

for tableName in splitfile:
    corrected = tableName.replace("`","")
    corrected = corrected.replace(",","")
    print ('<div><p>{{' + corrected +'form | safe}}</p></div>')

#do same for html code
#atr,chemicals,data_aquisition,depositor,dried_film,experiment,experimental_conditions,fourier_transform_processing,gas,liquid,molecular_composition,molecule,molecule_has_molecular_composition,not_atr,post_processing_and_deposited_spectra,project,project_has_experiment,protein,publication,publication_has_experiment,sample,solid,spectra,spectrometer,spectum,type/file,type,state_of_sample,transflectance/diffuse
