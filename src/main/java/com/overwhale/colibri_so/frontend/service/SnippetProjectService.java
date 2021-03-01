package com.overwhale.colibri_so.frontend.service;

import com.overwhale.colibri_so.backend.entity.SnippetProject;
import com.overwhale.colibri_so.backend.repository.SnippetProjectRepository;
import com.overwhale.colibri_so.frontend.dto.SnippetProjectDto;
import com.overwhale.colibri_so.frontend.mapper.SnippetProjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.util.Optional;
import java.util.UUID;

@Service
public class SnippetProjectService extends CrudService<SnippetProjectDto, UUID> {
  private final SnippetProjectRepository repository;

  public SnippetProjectService(@Autowired SnippetProjectRepository repository) {
    this.repository = repository;
  }

  public SnippetProjectDto update(SnippetProjectDto dto) {
    SnippetProject entity = SnippetProjectMapper.INSTANCE.dtoToEntiy(dto);
    return SnippetProjectMapper.INSTANCE.entityToDto(repository.save(entity));
  }

  @Override
  protected JpaRepository<SnippetProjectDto, UUID> getRepository() {
    return null;
  }

  public Optional<SnippetProjectDto> get(UUID id) {
    return repository.findById(id).map(e -> SnippetProjectMapper.INSTANCE.entityToDto(e));
  }

  public void delete(UUID id) {
    repository.deleteById(id);
  }

  public Page<SnippetProjectDto> list(Pageable pageable) {
    return repository.findAll(pageable).map(e -> SnippetProjectMapper.INSTANCE.entityToDto(e));
  }

  public int count() {
    return (int) repository.count();
  }
}
